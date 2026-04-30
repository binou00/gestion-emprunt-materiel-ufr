# Diagramme des cas d'utilisation (UML)

> Phase 1 — Conception. Identifie les acteurs et les interactions principales du système.

## Acteurs

- **Étudiant** : utilisateur principal, demande des emprunts.
- **Enseignant** : peut emprunter du matériel et superviser les étudiants.
- **Technicien** : gère le retour matériel, signale les pannes.
- **Administrateur** : valide les demandes, gère le catalogue, voit les statistiques.
- **Chatbot IA** : acteur système, répond aux questions sur le matériel.

## Diagramme (Mermaid)

```mermaid
flowchart LR
    subgraph Acteurs
        E((Étudiant))
        ENS((Enseignant))
        T((Technicien))
        A((Administrateur))
    end

    subgraph Système["Application — Gestion Emprunt Matériel"]
        UC1[S'inscrire / se connecter]
        UC2[Consulter le catalogue]
        UC3[Soumettre une demande<br/>d'emprunt]
        UC4[Localiser sur la carte]
        UC5[Suivre l'état de la demande]
        UC6[Discuter avec le chatbot IA]
        UC7[Restituer le matériel]
        UC8[Signaler une panne]
        UC9[Valider / refuser une demande]
        UC10[Gérer le catalogue CRUD]
        UC11[Gérer les utilisateurs]
        UC12[Voir le tableau de bord]
        UC13[Exporter des rapports]
    end

    E --> UC1
    E --> UC2
    E --> UC3
    E --> UC4
    E --> UC5
    E --> UC6
    E --> UC7

    ENS --> UC2
    ENS --> UC3
    ENS --> UC5

    T --> UC7
    T --> UC8

    A --> UC9
    A --> UC10
    A --> UC11
    A --> UC12
    A --> UC13

    UC3 -.include.-> UC4
    UC6 -.invoque.-> CB[(Service IA<br/>fine-tuned LLM)]
```

## Description textuelle des cas principaux

### UC3 — Soumettre une demande d'emprunt
- **Acteur** : Étudiant
- **Préconditions** : être authentifié.
- **Scénario nominal** :
  1. L'étudiant accède au catalogue.
  2. Il sélectionne un ou plusieurs matériels.
  3. Il saisit dates de début et de fin.
  4. Il indique l'emplacement d'utilisation (adresse + clic sur carte).
  5. Il valide ; la demande passe à l'état *en attente*.
- **Postconditions** : notification envoyée à l'admin.

### UC6 — Discuter avec le chatbot IA
- **Acteur** : Étudiant
- **Préconditions** : être authentifié.
- **Scénario nominal** :
  1. L'étudiant ouvre le chat.
  2. Il pose une question (ex. : "Comment mettre en station une station totale Leica TS06 ?").
  3. Le service IA renvoie une réponse fine-tunée.
  4. Si hors périmètre, redirection vers la documentation ou le responsable.

### UC9 — Valider / refuser une demande
- **Acteur** : Administrateur
- **Scénario** : consulte la file des demandes en attente, examine la disponibilité, approuve ou refuse en ajoutant un motif.
