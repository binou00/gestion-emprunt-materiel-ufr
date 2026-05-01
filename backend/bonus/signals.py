"""
Signals — envoient un e-mail quand une demande change de statut.

On s'appuie sur post_save pour suivre Demande, et on garde l'ancien statut
en mémoire grâce à pre_save (afin de détecter les transitions).
"""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from emprunts.models import Demande, Restitution, StatutDemande

logger = logging.getLogger(__name__)


# --- Capture du statut avant sauvegarde -------------------------------------
@receiver(pre_save, sender=Demande)
def memoriser_ancien_statut(sender, instance: Demande, **kwargs):
    """Stocke l'ancien statut sur l'instance pour comparaison post_save."""
    if instance.pk:
        try:
            ancien = Demande.objects.only("statut").get(pk=instance.pk)
            instance._ancien_statut = ancien.statut
        except Demande.DoesNotExist:
            instance._ancien_statut = None
    else:
        instance._ancien_statut = None


# --- Détection des transitions et envoi d'e-mail ----------------------------
@receiver(post_save, sender=Demande)
def notifier_changement_statut(sender, instance: Demande, created, **kwargs):
    ancien = getattr(instance, "_ancien_statut", None)

    # Cas 1 : création d'une nouvelle demande -> accusé de réception
    if created:
        _envoyer_email(
            destinataire=instance.utilisateur,
            sujet=f"[UFR SI] Demande #{instance.pk} reçue",
            corps=(
                f"Bonjour {instance.utilisateur.first_name or instance.utilisateur.username},\n\n"
                f"Votre demande d'emprunt #{instance.pk} a bien été enregistrée.\n"
                f"Elle sera examinée par un technicien dans les meilleurs délais.\n\n"
                f"Période demandée : du {instance.date_debut} au {instance.date_fin}.\n\n"
                "— Plateforme Gestion Matériel UFR SI"
            ),
        )
        return

    # Cas 2 : changement de statut sur demande existante
    if ancien and ancien != instance.statut:
        if instance.statut == StatutDemande.APPROUVEE:
            sujet = f"[UFR SI] Demande #{instance.pk} approuvée"
            corps = (
                f"Bonne nouvelle, votre demande d'emprunt #{instance.pk} a été approuvée.\n"
                f"Vous pouvez venir récupérer le matériel dès le {instance.date_debut}.\n\n"
                "— Plateforme Gestion Matériel UFR SI"
            )
        elif instance.statut == StatutDemande.REFUSEE:
            sujet = f"[UFR SI] Demande #{instance.pk} refusée"
            corps = (
                f"Votre demande d'emprunt #{instance.pk} a été refusée.\n"
                f"Motif : {instance.motif or '(non précisé)'}\n\n"
                "— Plateforme Gestion Matériel UFR SI"
            )
        elif instance.statut == StatutDemande.RESTITUEE:
            sujet = f"[UFR SI] Demande #{instance.pk} clôturée"
            corps = (
                f"La restitution du matériel pour la demande #{instance.pk} "
                "a bien été enregistrée. Merci !\n\n"
                "— Plateforme Gestion Matériel UFR SI"
            )
        else:
            return  # Pas de notification pour les autres transitions
        _envoyer_email(destinataire=instance.utilisateur, sujet=sujet, corps=corps)


# --- Helper d'envoi sécurisé ------------------------------------------------
def _envoyer_email(destinataire, sujet: str, corps: str) -> None:
    """Envoie un e-mail si le destinataire en a un. N'échoue jamais bruyamment."""
    if not getattr(destinataire, "email", None):
        logger.info("Pas d'email pour %s — notification ignorée.", destinataire)
        return
    try:
        send_mail(
            subject=sujet,
            message=corps,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@ufrsi.local"),
            recipient_list=[destinataire.email],
            fail_silently=True,
        )
        logger.info("Notification envoyée à %s : %s", destinataire.email, sujet)
    except Exception as exc:  # pragma: no cover
        logger.warning("Échec d'envoi e-mail à %s : %s", destinataire.email, exc)
