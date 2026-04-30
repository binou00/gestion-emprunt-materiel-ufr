# Script d'initialisation GitHub — Projet POO UFR SI
# Usage : ouvrir PowerShell dans ce dossier puis :
#         .\init_github.ps1
#
# Si l'exécution est bloquée par la politique de sécurité, lancer d'abord :
#         Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

$ErrorActionPreference = "Stop"

Write-Host "=== Initialisation Git pour le projet POO UFR SI ===" -ForegroundColor Cyan
Write-Host ""

# 1) Vérifier que git est installé
try {
    $gitVersion = git --version
    Write-Host "[OK] $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] Git n'est pas installé. Télécharge-le sur https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# 2) Demander l'URL du dépôt GitHub
Write-Host ""
Write-Host "Colle l'URL HTTPS de ton dépôt GitHub" -ForegroundColor Yellow
Write-Host "(exemple : https://github.com/binouhanne/gestion-emprunt-materiel-ufr.git)" -ForegroundColor DarkGray
$repoUrl = Read-Host "URL"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "[ERREUR] URL vide." -ForegroundColor Red
    exit 1
}

# 3) Configuration globale (si pas déjà fait)
$userName = git config --global user.name
$userEmail = git config --global user.email

if ([string]::IsNullOrWhiteSpace($userName)) {
    $name = Read-Host "Ton nom complet (pour les commits)"
    git config --global user.name "$name"
}
if ([string]::IsNullOrWhiteSpace($userEmail)) {
    git config --global user.email "binouhanne24@icloud.com"
}

Write-Host ""
Write-Host "Auteur des commits : $(git config --global user.name) <$(git config --global user.email)>" -ForegroundColor DarkGray
Write-Host ""

# 4) Initialiser le dépôt s'il n'existe pas déjà
if (Test-Path ".git") {
    Write-Host "[INFO] Dépôt git déjà initialisé. On continue." -ForegroundColor Yellow
} else {
    Write-Host "[1/5] git init..." -ForegroundColor Cyan
    git init -b main
}

# 5) git add + commit
Write-Host "[2/5] git add..." -ForegroundColor Cyan
git add .

Write-Host "[3/5] git commit..." -ForegroundColor Cyan
$commitMsg = "Phases 1 et 2 - Conception (UML, MCD/MLD) + Backend Django (modeles, API REST, fixtures materiel UFR)"
git commit -m "$commitMsg"

# 6) Brancher au remote
Write-Host "[4/5] git remote add origin..." -ForegroundColor Cyan
$existing = git remote 2>$null
if ($existing -contains "origin") {
    git remote set-url origin $repoUrl
} else {
    git remote add origin $repoUrl
}

# 7) Push
Write-Host "[5/5] git push..." -ForegroundColor Cyan
Write-Host ""
Write-Host ">>> GitHub va te demander de t'authentifier." -ForegroundColor Yellow
Write-Host "    - Login : ton pseudo GitHub" -ForegroundColor DarkGray
Write-Host "    - Mot de passe : un Personal Access Token" -ForegroundColor DarkGray
Write-Host "      (a creer ici : https://github.com/settings/tokens/new -> cocher 'repo')" -ForegroundColor DarkGray
Write-Host ""

git push -u origin main

Write-Host ""
Write-Host "=== TERMINE ! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Etapes suivantes :" -ForegroundColor Cyan
Write-Host "  1. Ouvre $repoUrl dans ton navigateur pour verifier"
Write-Host "  2. Settings -> Collaborators -> Add people"
Write-Host "     pour inviter Aminata Kounta sur le depot"
Write-Host "  3. Aminata clone avec : git clone $repoUrl"
Write-Host ""
