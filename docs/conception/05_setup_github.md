# Mise en ligne du projet sur GitHub

> Procédure à exécuter depuis le terminal Windows (PowerShell ou Git Bash).

## 1. Créer le dépôt sur GitHub (interface web)

1. Aller sur https://github.com/new
2. Nom du dépôt : `gestion-emprunt-materiel-ufr` (ou ce que vous voulez)
3. Description : *Application web Django + IA pour la gestion des emprunts de matériel topographique — Projet POO L2 Géomatique*
4. **Important** : NE PAS cocher "Add a README", "Add .gitignore" ni "License" (on a déjà tout en local).
5. Cliquer sur **Create repository**.
6. GitHub affichera l'URL du dépôt, par exemple :
   `https://github.com/<ton-pseudo>/gestion-emprunt-materiel-ufr.git`

## 2. Initialiser Git en local

Ouvrir **Git Bash** ou **PowerShell** dans le dossier du projet :

```bash
cd "C:\Users\binou\Documents\Projet POO"

# Configuration globale (à faire une seule fois sur ta machine, si pas déjà fait)
git config --global user.name "Ton Nom"
git config --global user.email "binouhanne24@icloud.com"

# Initialisation du dépôt
git init -b main
git add .
git commit -m "Phase 1 — Conception : structure, UML, MCD/MLD, architecture"
```

## 3. Lier au dépôt GitHub et pousser

```bash
git remote add origin https://github.com/<ton-pseudo>/gestion-emprunt-materiel-ufr.git
git push -u origin main
```

GitHub va te demander de t'authentifier. Deux options :

- **HTTPS + Personal Access Token** (recommandé) :
  - Créer un token : https://github.com/settings/tokens/new
  - Cocher la portée `repo`
  - Utiliser le token comme mot de passe au moment du push
- **SSH** : configurer une clé SSH (`ssh-keygen -t ed25519 -C "binouhanne24@icloud.com"`).

## 4. Ajouter le binôme comme collaborateur

Sur GitHub : `Settings` → `Collaborators` → `Add people` → entrer le pseudo du binôme.

Le binôme accepte l'invitation par email puis clone le dépôt :

```bash
git clone https://github.com/<ton-pseudo>/gestion-emprunt-materiel-ufr.git
```

## 5. Workflow de travail à deux (binôme)

```
Agent 1 (Backend/IA)         Agent 2 (Frontend/Carto)
       |                              |
   git pull                       git pull
       |                              |
   travaille                      travaille
   sur backend/                   sur frontend/
       |                              |
   git add backend/               git add frontend/
   git commit -m "..."            git commit -m "..."
   git push                       git push
```

**Bonnes pratiques** :
- Toujours `git pull` AVANT de commencer à coder.
- Chaque agent travaille de préférence sur son dossier (`backend/` vs `frontend/`) pour éviter les conflits.
- Pour les changements transverses : créer une branche (`git checkout -b feat/ma-fonctionnalite`), pousser, ouvrir une *Pull Request*.

## 6. Convention de messages de commit

```
feat:     nouvelle fonctionnalité    feat: ajout du modèle Demande
fix:      correction de bug          fix: validation des dates de demande
docs:     documentation               docs: mise à jour du README
style:    formatage                   style: indentation backend/users/views.py
refactor: réécriture sans changement refactor: extraction du service emprunt
test:     ajout de tests              test: tests unitaires du modèle Materiel
chore:    tâche annexe                chore: mise à jour de .gitignore
```
