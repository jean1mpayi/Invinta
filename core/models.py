from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid  # Pour générer des liens uniques

# ───────────────────────────────────────────────────────────────
# Liste des styles prédéfinis pour l'invitation
# ───────────────────────────────────────────────────────────────
STYLE_CHOICES = [
    ('classique', 'Classique'),
    ('moderne', 'Moderne'),
    ('mariage', 'Mariage'),
    ('anniversaire', 'Anniversaire'),
]

class Evenement(models.Model):
    organisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    date = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    style_invitation = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default='classique',
        help_text="Style visuel prédéfini pour l'invitation."
    )

    image_evenement = models.ImageField(
        upload_to='evenements/',
        null=True,
        blank=True,
        help_text="Image d'illustration de l’événement."
    )

    def __str__(self):
        return f"{self.titre} - {self.date.strftime('%d/%m/%Y')}"

class Invitation(models.Model):
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        related_name="invitations",
        help_text="Événement auquel cette invitation est liée."
    )
    nom_invite = models.CharField(max_length=100)
    email = models.EmailField()
    numero_telephone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Numéro de téléphone de l'invité."
    )
    statut = models.CharField(
        max_length=10,
        choices=[
            ("accepte", "Accepté"),
            ("refuse", "Refusé"),
            ("en_attente", "En attente")
        ],
        default="en_attente",
        help_text="Statut de la réponse de l'invité."
    )
    lien = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="Lien unique pour chaque invitation."
    )
    date_reponse = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date de réponse de l'invité (si disponible)."
    )

    def __str__(self):
        return f"{self.nom_invite} - {self.statut}"

    def get_absolute_url(self):
        """
        Renvoie l'URL pour afficher cette invitation (page publique).
        """
        return reverse('afficher_invitation', args=[self.id])