# Sélection du matériel à intégrer dans l'application

> Source : *Inventaire individuel contradictoire des matières – UFR Sciences de l'Ingénieur, 2023* (Comptable des matières : Khady NGOM).

## Critères de sélection

Le projet vise la **gestion d'emprunt du matériel topographique et géodésique**. Nous avons donc retenu :

1. **Le matériel de mesure** (stations totales, GNSS, niveaux).
2. **Les accessoires de terrain** indispensables à ce matériel (trépieds, embases, prismes, mires, supports).
3. **L'énergie** (batteries, chargeurs).
4. **Les outils de communication** (talkie-walkies — coordination sur le terrain).
5. **L'informatique mobile** (ordinateurs portables HP, tablettes Galaxy) car ils servent à acquérir et traiter les données de relevé.

Nous avons **exclu** :

- Le mobilier (chaises, tables, armoires, bureaux ministre, fauteuils).
- L'informatique fixe non transportable (Lenovo de salle, photocopieuses, vidéo-projecteurs fixes).
- Les consommables et fournitures (câbles HDMI, antivirus, casques de stock, rideaux).
- Les éléments hors-sujet (bouteille de gaz, coffre-fort, imprimantes A0).

## Bilan : 7 catégories, 23 matériels

| # | Catégorie | Matériels retenus | Quantité totale |
|---|-----------|------------------|-----------------|
| 1 | Stations totales | Leica TS06 (8), CTS-112 R4 (7), Géomesure (1) | 16 |
| 2 | Récepteurs GNSS / GPS | i50 (4), i73 (5), Garmin MAP 65S (20) | 29 |
| 3 | Niveaux et nivellement | Niveau électronique (1, en panne), niveau optique (8), mire 4m (9) | 18 |
| 4 | Accessoires de terrain | Trépied (42), embase GNSS (15), support prisme (2), prisme (22), canne GLS 11 (2), sonde (1) | 84 |
| 5 | Énergie | Batterie interne Leica (2), batterie externe GS14 (9), chargeur GKL221 (10), chargeur externe (7) | 28 |
| 6 | Communication | Paire de talkie-walkie (2 paires fonctionnelles) | 2 |
| 7 | Informatique mobile | HP Core i5 (4), HP Omen (3), Tablette Galaxy (50) | 57 |

**Total : 234 unités physiques** réparties sur 23 références matériel.

## Cas particuliers documentés

- **Niveau électronique numérique** : statut `EN_MAINTENANCE` (signalé en panne, acheminé à SWAN). Cas d'usage parfait pour démontrer le module *Maintenance*.
- **Niveau optique** : 8 disponibles sur 9 (1 en panne) → on illustre la gestion fine des unités défectueuses.
- **Talkie-walkie** : 6 paires inventoriées mais 4 défectueuses → quantité disponible réelle = 2.

Ces cas réalistes serviront à **valider** la fonctionnalité de gestion d'état (`DISPONIBLE` / `EN_MAINTENANCE` / `HORS_SERVICE`).

## Fichier d'initialisation Django

Les données ci-dessus sont disponibles au format **fixture Django** dans :

```
backend/fixtures/materiel_initial.json
```

Elles seront chargées en Phase 2 avec :

```bash
python manage.py loaddata materiel_initial.json
```
