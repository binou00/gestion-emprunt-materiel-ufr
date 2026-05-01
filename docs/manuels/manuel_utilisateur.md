# Manuel utilisateur — Plateforme de gestion d'emprunt du matériel UFR SI

**Université Iba Der Thiam de Thiès — UFR Sciences de l'Ingénieur**
Projet de Programmation Orientée Objet — Licence 2 Géomatique
Auteures : **Bineta Elimane Hanne** & **Aminata Kounta**

---

## Table des matières

1. Bienvenue
2. Premier accès
3. Catalogue du matériel
4. Faire une demande d'emprunt
5. Suivre mes demandes
6. Restitution
7. Assistant IA
8. Profils et rôles
9. Foire aux questions
10. Contact et support

---

## 1. Bienvenue

Cette plateforme permet aux étudiants, enseignants et techniciens de l'UFR Sciences de l'Ingénieur de gérer en ligne l'emprunt du matériel topographique et géodésique : stations totales, récepteurs GNSS, niveaux, accessoires, équipements informatiques mobiles.

Vous y trouverez :

- Un catalogue interactif du matériel disponible
- Un formulaire de demande avec géolocalisation sur carte
- Un suivi en temps réel du statut de vos demandes
- Un assistant IA pour répondre à vos questions techniques

L'objectif est de remplacer la gestion papier par un système traçable, transparent et accessible 24 h / 24.

## 2. Premier accès

### 2.1 Créer un compte

1. Ouvrez votre navigateur et allez sur l'adresse de la plateforme (par défaut : `http://127.0.0.1:8000`).
2. Cliquez sur le bouton **S'inscrire** en haut à droite.
3. Remplissez le formulaire d'inscription avec :
   - Votre **prénom** et votre **nom** (tels qu'ils apparaissent sur votre carte d'étudiant)
   - Votre **e-mail UFR** (utilisé pour les notifications)
   - Votre **filière** (par exemple « Géomatique L2 »)
   - Votre **niveau** (L2, L3, M1, M2)
   - Votre **téléphone** (optionnel, utile pour les urgences terrain)
   - Un **nom d'utilisateur** unique
   - Un **mot de passe robuste** (au moins 8 caractères, avec majuscules, chiffres et caractères spéciaux)
4. Cliquez sur **Créer mon compte**.

Votre compte est créé immédiatement avec le rôle **Étudiant**. Vous êtes connecté automatiquement.

### 2.2 Se connecter

1. Cliquez sur **Connexion** en haut à droite.
2. Entrez votre nom d'utilisateur et votre mot de passe.
3. Cliquez sur **Se connecter**.

Vous arrivez sur la page d'accueil avec accès complet aux fonctionnalités.

### 2.3 Se déconnecter

Cliquez sur votre prénom en haut à droite, puis sur **Se déconnecter**.

## 3. Catalogue du matériel

### 3.1 Consulter le catalogue

Cliquez sur **Catalogue** dans la barre de navigation. Vous voyez une grille de toutes les références disponibles à l'UFR.

Pour chaque matériel, vous trouvez :

- **Nom** et **modèle**
- **Catégorie** (Station totale, GNSS, Niveau, Accessoire, etc.)
- **État** (Disponible, Emprunté, Maintenance, Hors service)
- **Stock** (quantité disponible / quantité totale)

### 3.2 Filtrer par catégorie

Au-dessus de la grille, des boutons de filtre permettent d'afficher seulement les matériels d'une catégorie. Cliquez sur **Toutes** pour revenir à la vue complète.

### 3.3 Comprendre les états

| Pastille | Signification |
|----------|---------------|
| Vert « Disponible » | Au moins une unité libre, vous pouvez l'emprunter |
| Jaune « Emprunté » | Toutes les unités sont actuellement sorties |
| Bleu « Maintenance » | En réparation, indisponible temporairement |
| Gris « Hors service » | Définitivement indisponible |

## 4. Faire une demande d'emprunt

### 4.1 Accéder au formulaire

Cliquez sur **Nouvelle demande** dans la barre de navigation, ou sur le gros bouton vert depuis la page **Catalogue**.

### 4.2 Remplir les informations de période

Dans la première carte « Période d'emprunt » :

1. Choisissez la **date de début** : jour où vous récupérerez le matériel.
2. Choisissez la **date de fin** : jour où vous le rendrez. La date de fin est automatiquement contrainte à être supérieure ou égale à la date de début.
3. Saisissez le **motif** de la sortie : par exemple « TP de levé topographique encadré par M. Diallo », « Mémoire de fin d'études — site de Mboro », etc. **Soyez précis** : un motif vague risque de faire refuser votre demande.

### 4.3 Localiser votre zone de travail

Dans la carte « Localisation » :

1. La carte est centrée sur Thiès par défaut.
2. **Cliquez** à l'endroit exact où vous comptez utiliser le matériel. Un marqueur rouge apparaît.
3. Vous pouvez **glisser-déposer** ce marqueur pour ajuster sa position.
4. Les champs **Latitude** et **Longitude** se remplissent automatiquement.
5. Saisissez optionnellement un **nom de lieu** (ex : « Campus UFR SI », « Carrière de Pout »).

Cette géolocalisation aide les enseignants à comprendre votre besoin et permet à l'UFR de cartographier l'usage du matériel.

### 4.4 Sélectionner le matériel

Dans la carte de droite « Matériel à emprunter » :

1. Faites défiler la liste des équipements disponibles.
2. **Cochez** la case devant chaque matériel souhaité.
3. Le champ quantité s'active automatiquement. Saisissez la quantité voulue (limitée au stock disponible affiché).
4. Le compteur en haut à droite indique combien d'articles vous avez sélectionnés.

### 4.5 Soumettre

Cliquez sur le bouton vert **Soumettre ma demande**. Vous êtes redirigé vers **Mes demandes** où votre nouvelle demande apparaît avec le statut **En attente**.

### 4.6 Délais et bonnes pratiques

- Soumettez votre demande **au moins 48 heures** à l'avance.
- Pour un TP encadré ou un projet important : **une semaine** d'avance.
- En période d'examens, les ressources sont très sollicitées : prévoyez large.

## 5. Suivre mes demandes

### 5.1 Vue d'ensemble

Cliquez sur **Mes emprunts** dans la barre de navigation. Vous voyez un tableau récapitulant toutes vos demandes, de la plus récente à la plus ancienne.

### 5.2 Comprendre les statuts

| Statut | Signification | Action attendue de votre part |
|--------|---------------|-------------------------------|
| En attente | Soumise, attente de validation | Patientez (48 h ouvrées max) |
| Approuvée | Validée, prête à retirer | Rendez-vous au laboratoire pour retirer |
| Refusée | Refusée par le validateur | Lisez le motif, refaites une demande corrigée |
| En cours | Matériel retiré, sortie en cours | Rendez le matériel à la date prévue |
| Restituée | Matériel rendu, dossier clos | Rien à faire |
| Annulée | Annulée par vous-même | Rien à faire |

### 5.3 Voir les détails d'une demande

Cliquez sur le bouton **Détails** au bout de chaque ligne. Une zone se déplie en dessous avec :

- Le motif complet
- La liste des articles avec quantités
- Le lieu et les coordonnées GPS

### 5.4 Annuler une demande

Tant qu'une demande est en statut **En attente**, vous pouvez l'annuler. Une fois approuvée, vous devez contacter directement l'enseignant ou le technicien.

## 6. Restitution

### 6.1 Avant de venir rendre le matériel

Vérifiez que :

- Les **batteries** sont rechargées (utilisez les chargeurs fournis)
- Le matériel est **propre** : essuyez la poussière, vérifiez les optiques
- Les **trépieds** sont pliés, sangles serrées
- Les **prismes** sont rangés dans leur étui
- **Tous** les accessoires empruntés sont présents (cordons, télécommandes, mires, etc.)

### 6.2 À la restitution

Le technicien vérifie chaque article. Trois cas possibles pour chaque pièce :

- **Bon état** : le matériel revient en stock, rien à signaler.
- **Endommagé** : une fiche de maintenance est ouverte. Selon la nature et la cause du dommage, vous pouvez être amené à participer aux frais.
- **Perdu** : vous devez rembourser le matériel au prix de remplacement, après vérification (déclaration de perte, recherche).

### 6.3 En cas de retard

Un rappel automatique vous est envoyé. Sans justificatif valable, vous pouvez être suspendu temporairement de la plateforme et perdre la priorité sur vos prochaines demandes. **Prévenez toujours** le technicien dès que vous savez que vous serez en retard.

## 7. Assistant IA

### 7.1 Accéder à l'assistant

Cliquez sur **Assistant IA** dans la barre de navigation. Une fenêtre de discussion s'ouvre.

### 7.2 Poser une question

1. Tapez votre question dans le champ en bas (par exemple : « Quelle est la précision de la station Leica TS06 ? »).
2. Cliquez sur **Envoyer** ou pressez Entrée.
3. L'assistant répond en quelques secondes.

### 7.3 Que peut-il faire ?

L'assistant est entraîné sur :

- Les **fiches techniques** du matériel UFR (Leica TS06, Topcon CTS-112 R4, CHC i50/i73, Garmin, niveaux, etc.)
- Les **procédures** d'emprunt et de restitution
- Les **notions de topographie et géodésie** (angles, distances, nivellement, GNSS, projections UTM Sénégal)
- Les **questions fréquentes** des étudiants

### 7.4 Que ne peut-il pas faire ?

- Faire vos calculs de TP à votre place
- Répondre à des questions hors-périmètre (autres cours, vie universitaire en général)
- Remplacer un enseignant pour des questions de fond complexes
- Modifier vos demandes ou réserver du matériel pour vous

### 7.5 Conversations passées

La barre latérale gauche liste vos conversations passées. Cliquez sur l'une d'elles pour reprendre la discussion. Cliquez sur **Nouvelle** pour démarrer une discussion vierge.

## 8. Profils et rôles

La plateforme distingue quatre rôles, avec des permissions différentes.

### 8.1 Étudiant

C'est le rôle par défaut à l'inscription. Permet :

- Consulter le catalogue
- Soumettre des demandes
- Suivre ses propres demandes
- Discuter avec l'assistant IA

### 8.2 Enseignant

Attribué par un administrateur. Hérite des droits de l'étudiant et ajoute :

- Valider ou refuser les demandes des étudiants
- Voir toutes les demandes de sa filière

### 8.3 Technicien

Hérite des droits étudiant. Ajoute :

- Marquer les sorties et restitutions
- Ouvrir des fiches de maintenance
- Mettre à jour le stock

### 8.4 Administrateur

Tous les droits. Gère les utilisateurs, le catalogue, et accède au tableau de bord complet via `/admin/`.

## 9. Foire aux questions

**Q : J'ai oublié mon mot de passe.**
R : Contactez le technicien ou l'administrateur de l'UFR. Ils peuvent réinitialiser votre mot de passe manuellement. Une fonction « mot de passe oublié » par e-mail sera ajoutée prochainement.

**Q : Combien de matériels puis-je emprunter en même temps ?**
R : Pas de limite stricte, mais votre demande doit être justifiée. Le validateur peut refuser ou ajuster une demande qui mobilise trop de matériel.

**Q : Puis-je faire une demande pour mon binôme et moi ?**
R : Oui. Une seule demande, faite par le chef de binôme, avec les deux noms dans le motif.

**Q : Que se passe-t-il si du matériel tombe en panne pendant ma sortie ?**
R : Si vous prouvez une utilisation conforme, vous n'êtes pas responsable. Signalez la panne au technicien à la restitution. Une fiche de maintenance est ouverte automatiquement.

**Q : J'ai perdu un prisme, dois-je rembourser ?**
R : Oui, sauf cas de force majeure prouvé (vol avec dépôt de plainte). Le prix de remplacement vous sera communiqué par le technicien.

**Q : Le chatbot peut-il faire mes calculs de polygonale ?**
R : Il peut expliquer la méthode et les formules. Pour le calcul lui-même, utilisez Excel ou un logiciel dédié comme Covadis.

**Q : Mes données sont-elles confidentielles ?**
R : Oui. Seuls vous, l'enseignant validateur et le technicien voient vos demandes. Aucune donnée n'est partagée avec des tiers.

## 10. Contact et support

Pour signaler un bug, suggérer une amélioration, ou demander de l'aide :

- **Auteures du projet** : Bineta Elimane Hanne, Aminata Kounta
- **Dépôt GitHub** : ouvrir une issue sur le dépôt du projet
- **Sur place** : laboratoire de topographie de l'UFR SI

Bonne utilisation !

---

*Manuel utilisateur — version 1.0 — avril 2026.*
