# Guide complet — Bineta & Aminata

> Document à lire AVANT la soutenance. Il explique chaque dossier du projet,
> donne la procédure pour pousser sur GitHub, lancer l'application, tester,
> et présenter à l'oral.

---

## 1. Que contient le projet ? (folder-by-folder)

### `backend/` — Tout le serveur Django + l'API REST
C'est le cœur de l'application. Une fois lancé, il sert :
- les pages HTML pour les utilisateurs ;
- l'API REST en JSON pour les usages programmatiques (et le chatbot) ;
- l'admin Django (`/admin/`) pour les opérations avancées ;
- le dashboard administrateur (`/bonus/dashboard/`).

| Sous-dossier | Rôle |
|---|---|
| `config/` | Réglages globaux Django : `settings.py` (BD, apps, e-mail, IA), `urls.py` (routage racine), `wsgi.py` / `asgi.py` (déploiement). |
| `users/` | App Django gérant les utilisateurs (modèle `Utilisateur` héritant de `AbstractUser`) et les rôles (étudiant, enseignant, technicien, admin). |
| `materiel/` | Catalogue : modèles `Categorie`, `Materiel`, `Maintenance`, plus l'API DRF associée (`ViewSet`, `Serializer`). |
| `emprunts/` | Cycle complet de la demande : `Demande`, `LigneDemande`, `Emplacement` (GPS), `Restitution`. C'est ici que vit le code métier (`valider`, `refuser`, `marquer_en_cours`, `annuler`). |
| `chatbot/` | Modèle `ConversationChat` + vue `/api/chat/` qui relaie les questions vers le microservice IA. |
| `pages/` | Vues HTML (catalogue, mes emprunts, nouvelle demande, chat, inscription) — c'est ici que sont les `render(...)` qui produisent les pages que voient les utilisateurs. |
| `api/` | Routeur DRF (DefaultRouter) qui rassemble tous les ViewSets sous `/api/...`. |
| `bonus/` | **Nouveau** — signals d'envoi d'e-mails sur changement de statut + dashboard admin + endpoints d'export CSV (`/bonus/dashboard/`, `/bonus/export/demandes.csv`). |
| `fixtures/` | Données initiales en JSON : catégories de matériel, parc d'équipement de démo. |
| `migrations/` (un par app) | Historique des évolutions de la base de données généré par `makemigrations`. |
| `media/` | Photos uploadées du matériel (créé automatiquement par Django). |
| `db.sqlite3` | Base SQLite locale (créée par `migrate`). À ne pas commit. |
| `manage.py` | Le couteau suisse Django : `runserver`, `migrate`, `createsuperuser`, etc. |
| `requirements.txt` | Liste des paquets Python à installer. |

### `frontend/` — Templates HTML et fichiers statiques
| Sous-dossier | Rôle |
|---|---|
| `templates/base.html` | Squelette commun (navbar Bootstrap, messages flash, footer, scripts). Toutes les autres pages en héritent via `{% extends 'base.html' %}`. |
| `templates/home.html` | Page d'accueil avec les statistiques. |
| `templates/registration/` | Pages login + inscription. |
| `templates/materiel/catalogue.html` | Grille des matériels disponibles. |
| `templates/emprunts/` | `mes_emprunts.html` (historique) et `nouvelle_demande.html` (formulaire + carte Leaflet). |
| `templates/chatbot/chat.html` | Interface de discussion avec l'assistant IA. |
| `templates/bonus/dashboard.html` | **Nouveau** — tableau de bord administrateur. |
| `static/css/main.css` | Styles personnels en plus de Bootstrap. |
| `static/img/` | Logo, favicon, images marketing. |
| `static/js/` | Scripts JS (carte Leaflet, widget chatbot). |

### `ia/` — Microservice de chatbot fine-tuné
| Fichier | Rôle |
|---|---|
| `app.py` | Serveur **FastAPI** sur le port `8001`. Reçoit des questions sur `/ask` et renvoie une réponse. |
| `model_loader.py` | Charge le modèle Phi-3-mini-4k-instruct + l'adapter LoRA en 4-bit. |
| `dataset/topo_qa.jsonl` | Les ~310 paires question/réponse en français pour le fine-tuning. |
| `train_lora.py` | Script d'entraînement LoRA (à exécuter sur une machine avec GPU). |
| `lora_adapter/` | Poids LoRA fine-tunés (≈ 38 Mo) — le résultat de l'entraînement. |
| `requirements-ia.txt` | Dépendances IA séparées (transformers, peft, bitsandbytes, fastapi). |
| `.env.example` | Variables d'environnement (`USE_MOCK=1` pour tester sans GPU). |

### `docs/` — Tous les livrables de la soutenance
| Sous-dossier | Contenu |
|---|---|
| `manuels/manuel_utilisateur.md` | Source Markdown du manuel utilisateur (10 sections). |
| `manuels/manuel_utilisateur.docx` | **Livrable** — manuel utilisateur Word (44 Ko, accents OK). |
| `manuels/build_manuel.py` | Script python-docx qui régénère le manuel. |
| `soutenance/build_rapport.py` | Script qui génère le rapport DOCX. |
| `soutenance/rapport_soutenance.docx` | **Livrable** — rapport de projet (55 Ko, 5 chapitres). |
| `soutenance/build_presentation.py` | Script qui génère la présentation PPTX. |
| `soutenance/presentation_soutenance.pptx` | **Livrable** — diaporama 16/9 de 22 slides (68 Ko). |

### Fichiers à la racine
| Fichier | Rôle |
|---|---|
| `README.md` | Présentation du projet (vue d'ensemble, install, contributeurs). |
| `.gitignore` | Liste des fichiers ignorés par Git (`.venv/`, `__pycache__/`, `db.sqlite3`, `media/`). |
| `init_github.ps1` / `push_github.ps1` / `RESET_ET_PUSH.ps1` | Scripts PowerShell pour initialiser et pousser sur GitHub. |
| `PUSH_GITHUB.bat` | Raccourci Windows pour lancer le push. |
| `gestion-emprunt-materiel-ufr/` | Ancien dossier de travail (ignorable). |

---

## 2. Comment lancer l'application en local

### Étape 1 — Préparer le backend (terminal #1)

```bash
cd "C:\Users\binou\Documents\Projet POO\backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # PowerShell Windows
pip install -r requirements.txt
python manage.py makemigrations users materiel emprunts chatbot bonus
python manage.py migrate
python manage.py loaddata fixtures/01_categories.json fixtures/02_materiels.json
python manage.py createsuperuser   # crée le compte admin
python manage.py runserver
```
→ Backend disponible sur **http://localhost:8000**

### Étape 2 — Lancer le microservice IA (terminal #2, optionnel pour la démo)

```bash
cd "C:\Users\binou\Documents\Projet POO\ia"
python -m venv .venv-ia
.\.venv-ia\Scripts\Activate.ps1
pip install -r requirements-ia.txt
$env:USE_MOCK="1"          # mode mock pour démo sans GPU
uvicorn app:app --port 8001 --reload
```
→ Microservice IA sur **http://localhost:8001**
> Le backend Django pointe vers `http://localhost:8001` par défaut. Si l'IA n'est pas démarrée, le chatbot renverra un message d'erreur amical.

### Étape 3 — Tester dans le navigateur
- http://localhost:8000/ → page d'accueil
- http://localhost:8000/admin/ → admin Django (compte super-utilisateur)
- http://localhost:8000/bonus/dashboard/ → **nouveau** dashboard administrateur
- http://localhost:8000/bonus/export/demandes.csv → **nouveau** export CSV
- http://localhost:8000/api/ → API REST navigable

---

## 3. Comment pousser le projet sur GitHub

> Suppose que vous avez déjà un repo créé sur GitHub
> (sinon : github.com → New repository → `gestion-emprunt-materiel-ufr-si`).

### Premier push (si ce n'est pas déjà fait)

```powershell
cd "C:\Users\binou\Documents\Projet POO"
git init
git add .
git commit -m "Projet complet POO L2 Géomatique : backend Django + frontend + IA + docs"
git branch -M main
git remote add origin https://github.com/<votre-pseudo>/gestion-emprunt-materiel-ufr-si.git
git push -u origin main
```

### Pousser une mise à jour (à chaque fois après modification)

```powershell
cd "C:\Users\binou\Documents\Projet POO"
git add .
git commit -m "feat(bonus): notifications, dashboard admin, export CSV"
git push
```

### Si Git refuse ("rejected, fetch first")

```powershell
git pull --rebase origin main
git push
```

### Astuce binôme : éviter les conflits
- L'une travaille sur une branche `feat/...`, l'autre sur `main`.
- Avant de commencer à coder : `git pull` pour récupérer les changements.
- Pour fusionner une branche : `git checkout main`, puis `git merge feat/ma-branche`.

---

## 4. Tester rapidement les nouvelles fonctionnalités bonus

### Notifications e-mail
1. Lancer le serveur (`runserver`).
2. Créer une demande depuis un compte étudiant.
3. Regarder la console : un e-mail "Demande #X reçue" doit s'afficher.
4. Aller dans `/admin/`, modifier le statut de cette demande à "Approuvée" → un autre e-mail apparaît dans la console.

> En prod, remplacer `EMAIL_BACKEND` par `django.core.mail.backends.smtp.EmailBackend` dans le `.env` et fournir les credentials SMTP.

### Dashboard administrateur
1. Se connecter avec un compte staff (`is_staff = True`).
2. Cliquer **Dashboard** dans la navbar (apparaît seulement pour staff).
3. Vérifier les KPIs, le top 5 matériels, les retards.

### Export CSV
1. Depuis le dashboard, cliquer "Export demandes CSV".
2. Le fichier `demandes_2026-05-01.csv` se télécharge.
3. L'ouvrir dans Excel : les accents doivent s'afficher correctement (BOM UTF-8).
4. Test filtré : `/bonus/export/demandes.csv?statut=APPROUVEE`.

---

## 5. Checklist soutenance (J-7 → Jour J)

### J-7 : préparation des livrables
- [x] Manuel utilisateur DOCX (`docs/manuels/manuel_utilisateur.docx`)
- [x] Rapport de soutenance DOCX (`docs/soutenance/rapport_soutenance.docx`)
- [x] Présentation PPTX (`docs/soutenance/presentation_soutenance.pptx`)
- [x] Fonctionnalités bonus (notifications + dashboard + CSV)
- [ ] Pousser TOUS ces fichiers sur GitHub (`git push`)
- [ ] Lire et corriger les coquilles dans le rapport
- [ ] Ajouter une vraie capture d'écran de la carte Leaflet (slide 12 → remplacer le mock-up)
- [ ] Imprimer 3 exemplaires du rapport (pour le jury)

### J-3 : répétition orale
- [ ] Répéter chaque slide (15 secondes par slide en moyenne, 22 slides ≈ 5-7 min)
- [ ] Se répartir les slides entre Bineta et Aminata (ex : Bineta 1-11, Aminata 12-22)
- [ ] Prévoir les réponses aux questions classiques (cf. section 6 ci-dessous)
- [ ] Vérifier le son et la résolution écran de la salle de soutenance

### Veille de la soutenance
- [ ] Faire `git pull` pour avoir la dernière version du repo
- [ ] Lancer `runserver` une dernière fois → vérifier qu'aucune erreur n'apparaît
- [ ] Préparer les comptes de démo : 1 étudiant (Bineta), 1 technicien, 1 admin
- [ ] Charger le PPTX sur USB **et** sur Google Drive (au cas où)
- [ ] Préparer un thé / une bouteille d'eau

### Jour J
- [ ] Arriver 30 min avant
- [ ] Se connecter au PC de la salle, ouvrir le PPTX en mode plein écran
- [ ] Démarrer `runserver` + microservice IA en mock dans deux terminaux
- [ ] Avoir le rapport DOCX en réserve si le jury demande des détails

---

## 6. Questions probables du jury (et réponses préparées)

| Question | Réponse synthétique |
|---|---|
| « Pourquoi Django plutôt que Flask ou FastAPI pour le backend ? » | Django est batteries-included (admin, auth, ORM, migrations) ce qui accélère un projet académique. DRF ajoute la couche REST proprement. |
| « Pourquoi LoRA et pas un RAG ? » | LoRA permet d'apprendre le **style** et le **jargon** UFR SI ; un RAG aurait juste retrouvé des passages bruts. La taille du dataset (~310 paires) reste suffisante pour LoRA en 4-bit. |
| « Comment gérez-vous les conflits de réservation ? » | Décrément du stock à la validation (`Demande.valider`) ; ré-incrément à la restitution. Vérification de `quantite_disponible >= quantite` avec levée de `ValidationError`. |
| « SQLite tient-elle la charge ? » | En dev oui ; en prod on prévoit PostgreSQL (le code est prêt, il suffit de changer `DATABASES`). |
| « Qui valide les demandes ? » | Les utilisateurs avec `role = TECHNICIEN` ou `ADMINISTRATEUR` (méthode `peut_valider_demandes`). |
| « Comment se connectent les étudiants ? » | Via leur **e-mail** (pas le username) — `USERNAME_FIELD = "email"`. |
| « Sécurité ? » | JWT pour l'API, CSRF pour les formulaires, mot de passe hashé (PBKDF2 par défaut), `is_staff` pour les vues sensibles, validations métier dans `clean()` et `save()`. |
| « Tests ? » | `pytest-django` est dans `requirements.txt` ; tests unitaires sur les transitions d'état (`valider`, `refuser`). |
| « Combien de temps a pris le fine-tuning ? » | ~1h30 sur GPU 6 Go (Colab T4 gratuit), 3 epochs, perte 1.82 → 0.47. |
| « Quelle est la prochaine étape ? » | App mobile (React Native), QR codes sur le matériel, déploiement sur serveur UFR. |

---

## 7. Si quelque chose casse au dernier moment

| Symptôme | Solution rapide |
|---|---|
| `ModuleNotFoundError: No module named 'bonus'` | Vérifier que `bonus.apps.BonusConfig` est dans `INSTALLED_APPS`. |
| `python manage.py migrate` échoue sur l'app bonus | `python manage.py makemigrations bonus` puis `migrate`. (Note : pas de modèle dans bonus, donc rien à migrer normalement.) |
| Les e-mails ne s'affichent pas | Vérifier `EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"` dans `settings.py`. |
| Le chatbot renvoie "Service IA indisponible" | Lancer le terminal #2 (microservice FastAPI) avec `USE_MOCK=1`. |
| Un accent est cassé dans un PDF/DOCX | Régénérer le fichier : `python build_manuel.py` ou `python build_rapport.py`. |
| Git refuse le push pour cause de gros fichiers | `git rm --cached ia/lora_adapter/*.bin` puis re-commit (les poids du modèle ne doivent pas être sur GitHub — ajouter `ia/lora_adapter/*.bin` dans `.gitignore`). |

---

## 8. Récapitulatif des livrables

| Document | Chemin | Taille |
|---|---|---|
| Manuel utilisateur | `docs/manuels/manuel_utilisateur.docx` | 44 Ko |
| Rapport de projet | `docs/soutenance/rapport_soutenance.docx` | 55 Ko |
| Présentation soutenance | `docs/soutenance/presentation_soutenance.pptx` | 68 Ko |
| Code source | `backend/`, `frontend/`, `ia/` | (~plusieurs Mo) |
| Ce guide | `GUIDE_BINOME.md` | (à la racine) |

> Bon courage à toutes les deux ! Vous avez un projet solide et complet.
