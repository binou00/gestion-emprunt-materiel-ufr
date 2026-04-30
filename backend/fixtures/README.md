# Fixtures (données initiales)

À charger dans cet ordre :

```bash
python manage.py loaddata 01_categories.json
python manage.py loaddata 02_materiels.json
```

Ou en une seule commande :

```bash
python manage.py loaddata 01_categories.json 02_materiels.json
```

Le fichier `materiel_initial.json` est obsolète (vide). Il peut être supprimé.
