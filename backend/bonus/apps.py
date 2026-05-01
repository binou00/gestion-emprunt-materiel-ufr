"""Configuration de l'app bonus — branche les signaux au démarrage."""
from django.apps import AppConfig


class BonusConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bonus"
    verbose_name = "Bonus (notifications, dashboard, exports)"

    def ready(self):
        # Importe les signaux pour qu'ils soient enregistrés
        from . import signals  # noqa: F401
