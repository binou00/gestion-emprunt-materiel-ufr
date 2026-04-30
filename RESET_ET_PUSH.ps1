# ============================================================
# Script PowerShell — Nettoyage complet + Push GitHub propre
#
# Etapes :
#   1) Supprime le sous-dossier 'gestion-emprunt-materiel-ufr' (clone parasite)
#   2) Supprime le .git corrompu a la racine
#   3) Re-initialise git proprement
#   4) Commit
#   5) Push vers GitHub
#
# Avant de lancer : assure-toi d'avoir SUPPRIME le repo sur github.com
# (Settings -> Danger Zone -> Delete this repository)
# puis recreer un repo VIDE 'gestion-emprunt-materiel-ufr' (Private, sans README)
# ============================================================

$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   RESET + PUSH GITHUB - Projet POO UFR SI" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Confirmation préalable
Write-Host "AVANT DE CONTINUER, tu dois avoir :" -ForegroundColor Yellow
Write-Host "  1) Supprime le repo sur github.com (Settings > Danger Zone)" -ForegroundColor Yellow
Write-Host "  2) Recree un repo VIDE 'gestion-emprunt-materiel-ufr' sur github.com" -ForegroundColor Yellow
Write-Host "     (Private, NE COCHE RIEN : pas de README, pas de gitignore, pas de licence)" -ForegroundColor Yellow
Write-Host ""
$pret = Read-Host "C'est fait ? (o/n)"
if ($pret -ne "o" -and $pret -ne "O") {
    Write-Host "OK, fais-le d'abord et relance ce script." -ForegroundColor Yellow
    Read-Host "Appuie sur Entree pour quitter"
    exit 0
}

# 1) Supprimer le sous-dossier parasite
$sousRepo = Join-Path $PSScriptRoot "gestion-emprunt-materiel-ufr"
if (Test-Path $sousRepo) {
    Write-Host ""
    Write-Host "[1/5] Suppression du sous-dossier 'gestion-emprunt-materiel-ufr'..." -ForegroundColor Cyan
    try {
        Remove-Item -Recurse -Force $sousRepo
        Write-Host "[OK] Sous-dossier supprime" -ForegroundColor Green
    } catch {
        Write-Host "[ERREUR] Impossible de supprimer : $_" -ForegroundColor Red
        Write-Host "Essaie en mode admin ou fais-le manuellement dans l'explorateur." -ForegroundColor Yellow
        Read-Host "Appuie sur Entree pour quitter"
        exit 1
    }
} else {
    Write-Host "[1/5] Pas de sous-dossier parasite -> rien a faire" -ForegroundColor Green
}

# 2) Supprimer le .git corrompu
$dotGit = Join-Path $PSScriptRoot ".git"
if (Test-Path $dotGit) {
    Write-Host ""
    Write-Host "[2/5] Suppression du .git corrompu a la racine..." -ForegroundColor Cyan
    try {
        # On force, car .git contient des fichiers en lecture seule
        Get-ChildItem -Path $dotGit -Recurse -Force | ForEach-Object {
            $_.Attributes = 'Normal'
        }
        Remove-Item -Recurse -Force $dotGit
        Write-Host "[OK] .git supprime" -ForegroundColor Green
    } catch {
        Write-Host "[ERREUR] Impossible de supprimer .git : $_" -ForegroundColor Red
        Write-Host "Essaie en mode admin." -ForegroundColor Yellow
        Read-Host "Appuie sur Entree pour quitter"
        exit 1
    }
} else {
    Write-Host "[2/5] Pas de .git existant -> rien a faire" -ForegroundColor Green
}

# 3) Verifier Git
try {
    $null = git --version
} catch {
    Write-Host "[ERREUR] Git n'est pas installe. https://git-scm.com" -ForegroundColor Red
    Read-Host "Appuie sur Entree pour quitter"
    exit 1
}
$gitName  = git config --global user.name 2>$null
$gitEmail = git config --global user.email 2>$null
if (-not $gitName -or -not $gitEmail) {
    Write-Host ""
    if (-not $gitName)  { $gitName  = Read-Host "Ton nom complet" ;  git config --global user.name  "$gitName" }
    if (-not $gitEmail) { $gitEmail = Read-Host "Ton email" ;          git config --global user.email "$gitEmail" }
}

# 4) Demander pseudo GitHub
Write-Host ""
$githubUser = Read-Host "Ton pseudo GitHub"
$repoName = "gestion-emprunt-materiel-ufr"
$remoteUrl = "https://github.com/$githubUser/$repoName.git"
Write-Host "URL du depot : $remoteUrl" -ForegroundColor Cyan

# 5) Init + add + commit
Write-Host ""
Write-Host "[3/5] git init + add + commit..." -ForegroundColor Cyan
git init -b main | Out-Null
git add .
$staged = (git diff --cached --name-only | Measure-Object -Line).Lines
Write-Host "  $staged fichier(s) prets a etre commit" -ForegroundColor Green

$commitMessage = @"
Phases 1 + 2 - Conception et Backend Django

Phase 1 - Conception
  - README, diagrammes UML (cas d'utilisation, classes)
  - MCD / MLD (Merise)
  - Architecture technique en couches
  - Selection du materiel (inventaire UFR_SI 2023)

Phase 2 - Backend Django + API REST
  - 4 apps Django : users, materiel, emprunts, chatbot
  - Modele Utilisateur custom avec roles
  - Cycle d'emprunt complet avec methodes metier
  - API REST DRF + auth JWT + admin Django
  - Fixtures : 7 categories + 23 materiels topographiques

Binome :
  - Bineta Elimane Hanne (Backend & IA)
  - Aminata Kounta (Frontend & Cartographie)
"@

git commit -m "$commitMessage" | Out-Null
Write-Host "[OK] Commit cree" -ForegroundColor Green

# 6) Remote + push
Write-Host ""
Write-Host "[4/5] Liaison au depot GitHub..." -ForegroundColor Cyan
git remote add origin $remoteUrl
Write-Host "[OK] Remote configure" -ForegroundColor Green

Write-Host ""
Write-Host "[5/5] Push vers GitHub..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Si Git demande un mot de passe, utilise un Personal Access Token :" -ForegroundColor Yellow
Write-Host "  https://github.com/settings/tokens/new (cocher 'repo')" -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "   SUCCES !" -ForegroundColor Green
    Write-Host "   https://github.com/$githubUser/$repoName" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "N'oublie pas d'ajouter Aminata Kounta comme collaboratrice :" -ForegroundColor Cyan
    Write-Host "  GitHub > Settings > Collaborators > Add people" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERREUR] Le push a echoue." -ForegroundColor Red
    Write-Host "Verifie :" -ForegroundColor Yellow
    Write-Host "  - Le repo $repoName est-il bien cree (et VIDE) sur GitHub ?" -ForegroundColor Yellow
    Write-Host "  - As-tu utilise un Personal Access Token comme mot de passe ?" -ForegroundColor Yellow
    Write-Host "  - Le pseudo GitHub est-il correct ?" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Appuie sur Entree pour quitter"
