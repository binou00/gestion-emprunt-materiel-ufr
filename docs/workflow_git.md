# Workflow Git en binôme

> Convention de travail à respecter pour éviter les conflits.

## Branches

- `main` → version stable, ne jamais y pousser directement.
- `feat/backend` → branche de Bineta (Backend & IA).
- `feat/frontend` → branche d'Aminata (Frontend & Carto).
- `feat/<courte-description>` → branche pour une fonctionnalité ponctuelle (ex: `feat/dashboard-admin`).

## Première mise en place (à faire chacune sur son ordi)

### Bineta (Backend)

```bash
git pull
git checkout -b feat/backend
git push -u origin feat/backend
```

### Aminata (Frontend)

```bash
git clone https://github.com/<pseudo-bineta>/gestion-emprunt-materiel-ufr.git
cd gestion-emprunt-materiel-ufr
git checkout -b feat/frontend
git push -u origin feat/frontend
```

## Routine quotidienne

Avant de commencer à coder :

```bash
git checkout main
git pull
git checkout feat/<ma-branche>
git merge main           # récupère les dernières nouveautés du main
```

À la fin de la journée :

```bash
git add .
git commit -m "feat: <description courte>"
git push
```

## Pour intégrer son travail dans `main`

Quand une fonctionnalité est prête :

1. Aller sur GitHub → onglet **Pull requests** → **New pull request**
2. `base: main` ← `compare: feat/frontend` (ou `feat/backend`)
3. Titre clair, description de ce qui change
4. Demander à l'autre membre de relire (review)
5. **Merge pull request** quand validé

## Convention de messages de commit

```
feat:     nouvelle fonctionnalité    feat: ajout du modele Demande
fix:      correction de bug          fix: validation des dates
docs:     documentation               docs: mise a jour du README
style:    formatage / CSS             style: navbar Bootstrap
refactor: réécriture                  refactor: extraction du service emprunt
test:     ajout de tests              test: tests modele Materiel
chore:    tâche annexe                chore: maj .gitignore
```

## En cas de conflit

```bash
git status                    # voir les fichiers en conflit
# ouvrir chaque fichier en conflit, chercher les marqueurs <<<<<<<
# choisir la bonne version, supprimer les marqueurs
git add <fichier-resolu>
git commit
git push
```

Si tu es perdue : **NE FAIS RIEN, demande de l'aide**. Les conflits Git mal résolus peuvent perdre du travail.

## Règles d'or

1. **Toujours `git pull` avant de coder.**
2. **Ne pas pousser directement sur `main`.**
3. **Petits commits fréquents** plutôt qu'un énorme commit en fin de journée.
4. **Messages de commit en français, à l'impératif** : "ajoute la page connexion" plutôt que "ajout".
5. **Chacune dans son dossier** : Bineta touche surtout `backend/`, Aminata surtout `frontend/`. Les fichiers transverses (README, settings) → toujours `git pull` avant.
