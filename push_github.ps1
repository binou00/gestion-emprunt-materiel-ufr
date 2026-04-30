# ============================================================
# Script PowerShell — Initialise Git et pousse le projet sur GitHub
# Usage : clic droit > "Exécuter avec PowerShell"
#   ou  : ouvrir PowerShell dans ce dossier puis taper .\push_github.ps1
# ============================================================

$ErrorActionPreference = "Stop"

# Se positionner dans le dossier du script
Set-Location -Path $PSScriptRoot

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   PUSH GITHUB - Projet POO Gestion Emprunt Materiel UFR" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 1) Vérifier que Git est installé
try {
    $gitVersion = git --version
    Write-Host "[OK] $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] Git n'est pas installe. Telecharge-le sur https://git-scm.com" -ForegroundColor Red
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}

# 2) Vérifier la config Git
$gitName  = git config --global user.name 2>$null
$gitEmail = git config --global user.email 2>$null

if (-not $gitName -or -not $gitEmail) {
    Write-Host ""
    Write-Host "Configuration Git manquante. On la configure :" -ForegroundColor Yellow
    if (-not $gitName) {
        $gitName = Read-Host "  Ton nom complet (ex: Bineta Hanne)"
        git config --global user.name "$gitName"
    }
    if (-not $gitEmail) {
        $gitEmail = Read-Host "  Ton email (ex: binouhanne24@icloud.com)"
        git config --global user.email "$gitEmail"
    }
}
Write-Host "[OK] Git configure : $gitName <$gitEmail>" -ForegroundColor Green

# 3) Demander le pseudo GitHub
Write-Host ""
$githubUser = Read-Host "Ton pseudo GitHub"
$repoName = "gestion-emprunt-materiel-ufr"
$remoteUrl = "https://github.com/$githubUser/$repoName.git"

Write-Host ""
Write-Host "URL du depot : $remoteUrl" -ForegroundColor Cyan
$confirm = Read-Host "OK ? (o/n)"
if ($confirm -ne "o" -and $confirm -ne "O" -and $confirm -ne "y") {
    Write-Host "Annule." -ForegroundColor Yellow
    exit 0
}

# 4) Initialiser le dépôt s'il n'existe pas
if (-not (Test-Path ".git")) {
    Write-Host ""
    Write-Host "[1/5] Initialisation du depot Git..." -ForegroundColor Cyan
    git init -b main
    Write-Host "[OK] Depot initialise" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[1/5] Depot Git deja initialise" -ForegroundColor Green
}

# 5) Ajouter tous les fichiers
Write-Host ""
Write-Host "[2/5] Ajout des fichiers..." -ForegroundColor Cyan
git add .
$staged = git diff --cached --name-only | Measure-Object -Line
Write-Host "[OK] $($staged.Lines) fichier(s) ajoute(s)" -ForegroundColor Green

# 6) Commit
Write-Host ""
Write-Host "[3/5] Creation du commit..." -ForegroundColor Cyan
$commitMessage = @"
Phases 1 + 2 - Conception et Backend Django

Phase 1 - Conception
  - README projet et binome
  - Diagramme de cas d'utilisation (UML)
  - Diagramme de classes (UML)
  - MCD / MLD (Merise)
  - Architecture technique en couches
  - Selection du materiel (issu de l'inventaire UFR_SI 2023)

Phase 2 - Backend Django + API REST
  - Configuration Django (settings, urls, wsgi)
  - App users : Utilisateur custom avec roles
  - App materiel : Categorie, Materiel, Maintenance
  - App emprunts : Demande, LigneDemande, Emplacement, Restitution
                   avec methodes metier (valider, refuser, annuler)
  - App chatbot : ConversationChat + ChatService (mock pour Phase 5)
  - API REST DRF avec auth JWT
  - Admin Django avec actions rapides
  - Fixtures : 7 categories + 23 materiels topographiques

Binome :
  - Bineta Elimane Hanne (Backend & IA)
  - Aminata Kounta (Frontend & Cartographie)
"@

# Évite l'erreur si rien à commiter
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "[OK] Aucun changement a commiter" -ForegroundColor Yellow
} else {
    git commit -m "$commitMessage"
    Write-Host "[OK] Commit cree" -ForegroundColor Green
}

# 7) Lier au dépôt distant
Write-Host ""
Write-Host "[4/5] Liaison au depot GitHub..." -ForegroundColor Cyan
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    if ($existingRemote -ne $remoteUrl) {
        Write-Host "  Mise a jour du remote existant : $existingRemote -> $remoteUrl" -ForegroundColor Yellow
        git remote set-url origin $remoteUrl
    } else {
        Write-Host "[OK] Remote deja configure" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "[OK] Remote ajoute : $remoteUrl" -ForegroundColor Green
}

# 8) Push
Write-Host ""
Write-Host "[5/5] Push vers GitHub..." -ForegroundColor Cyan
Write-Host ""
Write-Host "GitHub va te demander de t'authentifier." -ForegroundColor Yellow
Write-Host "Si c'est ta premiere fois sur cette machine, utilise un Personal Access Token :" -ForegroundColor Yellow
Write-Host "  1. Va sur https://github.com/settings/tokens/new" -ForegroundColor Yellow
Write-Host "  2. Coche 'repo' dans les scopes" -ForegroundColor Yellow
Write-Host "  3. Genere et copie le token" -ForegroundColor Yellow
Write-Host "  4. Utilise-le comme MOT DE PASSE quand Git le demandera" -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "   SUCCES ! Projet pousse sur GitHub" -ForegroundColor Green
    Write-Host "   https://github.com/$githubUser/$repoName" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Prochaines etapes :" -ForegroundColor Cyan
    Write-Host "  - Va sur ton depot et verifie que tout est bien pousse" -ForegroundColor White
    Write-Host "  - Ajoute Aminata Kounta comme collaboratrice :" -ForegroundColor White
    Write-Host "    Settings > Collaborators > Add people > son pseudo GitHub" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERREUR] Le push a echoue." -ForegroundColor Red
    Write-Host "Verifie :" -ForegroundColor Yellow
    Write-Host "  - As-tu bien cree le depot $repoName sur GitHub ?" -ForegroundColor Yellow
    Write-Host "  - As-tu utilise un Personal Access Token comme mot de passe ?" -ForegroundColor Yellow
    Write-Host "  - Le pseudo GitHub est-il correct ?" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Appuie sur Entree pour quitter"
