# Corpus — Notions de topographie & géodésie

Source : cours L1/L2 Géomatique UFR SI, manuels classiques.

## Définitions de base

### Topographie
Science qui a pour but la mesure puis la représentation graphique d'une portion de la surface terrestre, en y figurant le relief et les détails (naturels ou artificiels).

### Géodésie
Science qui étudie la forme et les dimensions de la Terre, ainsi que son champ de pesanteur. Fournit les systèmes de référence (géoïde, ellipsoïde) sur lesquels s'appuie la topographie.

### Géomatique
Discipline qui regroupe l'ensemble des outils et méthodes permettant d'acquérir, de représenter, d'analyser et d'intégrer des données géographiques (topographie, SIG, télédétection, GNSS).

## Mesure des angles

### Angle horizontal
Mesuré dans le plan horizontal, entre deux directions de visée. Permet de calculer la position planimétrique d'un point.

### Angle vertical (zénithal ou de site)
Mesuré dans le plan vertical, par rapport au zénith (zénithal) ou à l'horizontale (site). Sert au calcul de dénivelée et de distance horizontale.

### Précision attendue
- Théodolite optique : 10" à 20"
- Station totale courante : 5" (Leica TS06)
- Station totale de précision : 1" à 2" (Topcon CTS-112 R4)

## Mesure des distances

### Distance inclinée (Di)
Mesurée directement par l'onde infrarouge ou laser entre la station et le prisme.

### Distance horizontale (Dh)
Calculée : `Dh = Di × sin(angle zénithal)`. C'est elle qui sert pour le plan.

### Dénivelée (Δh)
Calculée : `Δh = Di × cos(angle zénithal) + h_station - h_prisme`.

## Nivellement

### Nivellement direct (géométrique)
Utilise un niveau optique ou électronique et une mire. Mesure la différence d'altitude entre deux points en lisant la mire posée successivement sur chacun.
**Principe** : `Δh = lecture_arrière - lecture_avant`

### Nivellement indirect (trigonométrique)
Utilise une station totale. Calcule la dénivelée à partir de l'angle vertical et de la distance.
**Précision** : moindre que le nivellement direct sur courtes distances.

### Cheminement
Suite d'opérations de nivellement entre un point connu et un point à déterminer, avec contrôle par fermeture (aller-retour ou polygone fermé).

## Polygonale

Suite de stations reliées par des visées, formant une chaîne (ouverte ou fermée). Chaque station mesure les angles et distances vers la suivante.
- **Fermeture** : la somme des angles doit être proche de la valeur théorique (ex : 180° × (n-2) pour un polygone fermé à n côtés).
- **Tolérance** : dépend de la classe de levé (1ère, 2ème, 3ème classe).

## GNSS — Modes de positionnement

### Statique
Long temps d'observation (1 h à 24 h). Précision millimétrique après post-traitement. Pour réseaux de référence.

### RTK (Real-Time Kinematic)
Mode temps réel avec correction par radio ou GSM depuis une base. Précision 1-2 cm. Utilisé par les i50 et i73 de l'UFR.

### PPK (Post-Processing Kinematic)
Cinématique avec post-traitement. Bonne précision sans liaison radio.

### DGPS / SBAS
Correction différentielle (EGNOS, WAAS). Précision sub-métrique. Modes des Garmin GPSMAP 65S.

## Systèmes de référence

### Sénégal
- **Géodésique** : ITRF/IGS (international) ou réseau national AFREF
- **Projection** : UTM zone 28N (longitude -18° à -12°)
- **Altitudes** : réseau de nivellement IGN-Sénégal, référence à Dakar

### Coordonnées UTM (Universal Transverse Mercator)
- Plan de projection en mètres (X, Y)
- Découpage en fuseaux de 6° de longitude
- Le Sénégal est dans les fuseaux 28N et 29N

## Erreurs et précisions

### Erreur systématique
Reproductible, due à un défaut de l'instrument (ex : collimation mal réglée). Se corrige par étalonnage.

### Erreur accidentelle
Aléatoire, due à l'opérateur ou aux conditions (vent, vibration). Se réduit en multipliant les mesures.

### Erreur grossière
Faute (mauvaise lecture, point mal pointé). Se détecte par contrôle (double lecture, fermeture).

## Bonnes pratiques de terrain

- **Toujours stationner** avec embase et plomb optique vérifiés
- **Vérifier la constante de prisme** avant toute mesure
- **Faire des doubles retournements** (CG/CD) pour éliminer la collimation
- **Boucler son cheminement** pour contrôler les erreurs
- **Noter les conditions** (météo, opérateur, instrument) sur le carnet de terrain
