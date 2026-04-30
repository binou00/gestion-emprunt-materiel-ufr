# Diagramme de classes (UML)

> Phase 1 — Conception. Vue orientée objet du domaine métier. Cette structure guidera directement l'écriture des modèles Django en Phase 2.

## Diagramme (Mermaid)

```mermaid
classDiagram
    class Utilisateur {
        +int id
        +string nom
        +string prenom
        +string email
        +string telephone
        +string filiere
        +string niveau
        +Role role
        +seConnecter()
        +modifierProfil()
    }

    class Role {
        <<enumeration>>
        ETUDIANT
        ENSEIGNANT
        TECHNICIEN
        ADMINISTRATEUR
    }

    class Categorie {
        +int id
        +string libelle
        +string description
    }

    class Materiel {
        +int id
        +string nom
        +string numeroSerie
        +EtatMateriel etat
        +string photo
        +string description
        +date dateAcquisition
        +estDisponible() bool
        +marquerEnPanne()
    }

    class EtatMateriel {
        <<enumeration>>
        DISPONIBLE
        EMPRUNTE
        EN_MAINTENANCE
        HORS_SERVICE
    }

    class Demande {
        +int id
        +date dateDemande
        +date dateDebut
        +date dateFin
        +Statut statut
        +string motif
        +valider()
        +refuser(motif)
        +annuler()
    }

    class Statut {
        <<enumeration>>
        EN_ATTENTE
        APPROUVEE
        REFUSEE
        EN_COURS
        RESTITUEE
    }

    class LigneDemande {
        +int id
        +int quantite
    }

    class Emplacement {
        +int id
        +string libelle
        +float latitude
        +float longitude
        +string adresse
    }

    class Restitution {
        +int id
        +date dateRetour
        +EtatMateriel etatRetour
        +string observations
    }

    class Maintenance {
        +int id
        +string type
        +date dateSignalement
        +date dateResolution
        +string statut
    }

    class ConversationChat {
        +int id
        +datetime date
        +json messages
        +ajouterMessage(role, contenu)
    }

    Utilisateur "1" -- "1" Role
    Utilisateur "1" --> "*" Demande : soumet
    Utilisateur "1" --> "*" ConversationChat : initie

    Materiel "*" -- "1" Categorie
    Materiel "1" --> "*" Maintenance : subit
    Materiel "1" -- "1" EtatMateriel

    Demande "1" -- "1" Statut
    Demande "1" --> "*" LigneDemande : contient
    Demande "1" --> "1" Emplacement : utilise
    Demande "1" --> "0..1" Restitution : conclut
    LigneDemande "*" --> "1" Materiel
```

## Cardinalités principales

| Relation | Cardinalité | Sens |
|----------|-------------|------|
| Utilisateur — Demande | 1..* | Un utilisateur peut faire plusieurs demandes |
| Demande — LigneDemande | 1..* | Une demande contient plusieurs lignes (matériels différents) |
| LigneDemande — Matériel | * — 1 | Une ligne référence un seul matériel |
| Demande — Emplacement | 1 — 1 | Une demande a un et un seul emplacement |
| Demande — Restitution | 1 — 0..1 | Restitution optionnelle (existe seulement après retour) |
| Matériel — Catégorie | * — 1 | Un matériel appartient à une catégorie |
| Matériel — Maintenance | 1..* | Un matériel peut avoir plusieurs maintenances |

## Justifications de conception

- **Enum `Role`, `Statut`, `EtatMateriel`** : valeurs fermées, contrôlées au niveau modèle (en Django : `choices`).
- **`LigneDemande` (table d'association)** : permet d'emprunter plusieurs matériels en une seule demande, avec des quantités.
- **`Emplacement` séparé** : on pourra plus tard avoir plusieurs emplacements par demande (mission de plusieurs jours), évolutif.
- **`ConversationChat`** : stockage JSON des messages pour rester souple et faciliter l'export vers un fichier d'apprentissage.
