# Architecture générale du système

> Phase 1 — Conception. Vue technique : composants, flux, déploiement.

## 1. Vue d'ensemble (architecture en couches)

```mermaid
flowchart TB
    subgraph Client["Client (navigateur)"]
        UI[Interface utilisateur<br/>HTML/CSS/Bootstrap 5]
        JS[JavaScript<br/>Leaflet.js, fetch API]
    end

    subgraph Serveur["Serveur Django"]
        VIEWS[Vues Django<br/>Templates]
        DRF[Django REST Framework<br/>API JSON]
        AUTH[Authentification<br/>Sessions / Token]
        BL[Logique métier<br/>Services]
        ORM[ORM Django]
    end

    subgraph IA["Service IA"]
        API_IA[API FastAPI<br/>endpoint /chat]
        LLM[LLM fine-tuné<br/>Mistral 7B + LoRA]
        RAG[Retriever RAG<br/>FAISS / BM25]
        DOCS[(Corpus de docs<br/>manuels, FAQ)]
    end

    DB[(SQLite / PostgreSQL<br/>+ PostGIS)]

    UI --> JS
    JS -- "HTTP/JSON" --> DRF
    UI -- "HTTP" --> VIEWS
    VIEWS --> AUTH
    DRF --> AUTH
    AUTH --> BL
    BL --> ORM
    ORM --> DB

    JS -- "/api/chat" --> DRF
    DRF -- "asynchrone" --> API_IA
    API_IA --> LLM
    API_IA --> RAG
    RAG --> DOCS
```

## 2. Choix techniques justifiés

| Couche | Choix | Justification |
|--------|-------|---------------|
| Backend | Django + DRF | Robuste, ORM puissant, admin auto-généré, écosystème mûr |
| Front | Bootstrap 5 + JS vanilla | Léger, pas de build complexe, suffisant pour le périmètre |
| Carto | Leaflet.js + OSM | Open source, simple à intégrer, gratuit |
| BDD | SQLite (dev), PostgreSQL+PostGIS (prod) | SQLite pour simplifier le setup local ; PostGIS pour la recherche spatiale en prod |
| IA | LoRA/QLoRA via Hugging Face | Réduit drastiquement les besoins GPU (4-bit), permet l'entraînement sur Colab gratuit |
| Service IA | FastAPI séparé | Découplage : on peut redémarrer le LLM sans toucher Django |

## 3. Découpage en applications Django

```
backend/
├── config/              # settings, urls, wsgi
├── users/               # Utilisateur custom (rôles)
├── materiel/            # Matériel, Catégorie, Maintenance
├── emprunts/            # Demande, LigneDemande, Emplacement, Restitution
├── chatbot/             # ConversationChat + client vers API IA
└── api/                 # Routage DRF (regroupe les viewsets)
```

**Principe** : une *app Django par domaine fonctionnel*, pour rester modulaire et testable.

## 4. Flux nominal — "Soumettre une demande"

```mermaid
sequenceDiagram
    actor E as Étudiant
    participant F as Frontend (JS)
    participant D as Django (DRF)
    participant DB as Base SQLite

    E->>F: Remplit formulaire + clique sur la carte
    F->>D: POST /api/demandes/ {materiels, dates, lat, lng}
    D->>D: Validation : disponibilité, dates cohérentes
    D->>DB: INSERT Demande, LigneDemande, Emplacement
    D->>F: 201 Created {id, statut: EN_ATTENTE}
    F->>E: Affiche confirmation + redirige vers historique
```

## 5. Flux IA — "Question au chatbot"

```mermaid
sequenceDiagram
    actor E as Étudiant
    participant F as Frontend (chat)
    participant D as Django
    participant IA as Service FastAPI
    participant LLM as Modèle fine-tuné

    E->>F: "Comment caler une station Leica TS06 ?"
    F->>D: POST /api/chat/ {question, conversation_id}
    D->>D: Sauvegarde le message dans ConversationChat
    D->>IA: POST /chat {prompt, history}
    IA->>LLM: Inférence (génération)
    LLM-->>IA: Réponse texte
    IA-->>D: {answer}
    D->>D: Sauvegarde la réponse
    D-->>F: {answer}
    F-->>E: Affiche la réponse
```

## 6. Principes POO appliqués

- **Encapsulation** : chaque modèle expose des méthodes métier (`Demande.valider()`) plutôt que de manipuler les attributs depuis l'extérieur.
- **Héritage** : `Utilisateur` hérite de `AbstractUser` Django pour ajouter `role`, `filiere`, `niveau`.
- **Polymorphisme** : la méthode `__str__()` est redéfinie sur chaque modèle pour un affichage cohérent dans l'admin.
- **Abstraction** : la couche IA est isolée derrière une interface `ChatService` — on peut remplacer le modèle sans toucher au reste.

## 7. Sécurité

- Authentification par session Django (cookies HttpOnly).
- CSRF activé par défaut sur toutes les vues POST.
- Hashage des mots de passe via `PBKDF2` (par défaut Django).
- Permissions DRF : `IsAuthenticated` partout, `IsAdminUser` pour les endpoints d'administration.
- Pas de secrets en dur : toutes les clés dans `.env` (jamais commit).
