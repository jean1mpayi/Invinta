from django.contrib import admin
from .models import Evenement, Invitation
from django.utils.html import format_html  # Pour afficher du HTML dans l'admin
from django.urls import reverse


# ================================
# Admin personnalisé pour Evenement
# ================================
class EvenementAdmin(admin.ModelAdmin):
    # Ce qui s'affiche dans la liste admin des événements
    list_display = ('titre', 'date', 'lieu', 'organisateur')


# ================================
# Admin personnalisé pour Invitation
# ================================ 
@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    # Champs visibles dans la liste admin
    list_display = ('nom_invite', 'email', 'statut', 'evenement', 'lien_partage')
    list_filter = ('statut',)  # Filtre à droite dans l’admin (accepte / refuse / etc.)
    search_fields = ('nom_invite', 'email')  # Barre de recherche dans l’admin

    def lien_partage(self, obj):
        """
        Retourne un lien complet que l’admin peut copier ou cliquer pour voir
        l’invitation côté invité.
        """
        # URL relative générée automatiquement par Django
        url = obj.get_absolute_url()

        # URL complète locale pour test ()
        full_url = f"http://127.0.0.1:8000{url}"

        # HTML cliquable
        return format_html(f'<a href="{full_url}" target="_blank">{full_url}</a>')

    lien_partage.short_description = "Lien à partager"  # Nom de colonne dans l’admin
    
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'lieu', 'organisateur', 'voir_invitations', 'image_evenement')
    donly_fields = ('image_evenement_preview')
    
    def image_evenement_preview(self, obj) :
        if obj.images_evenement :
            return f'<img src="{obj.image_evenement.url}" width="200"/>'
        return "(Aucune image)"
    image_evenement_preview.allow_tags = True
    image_evenement_preview.short_description = "Aperçu de l'image"

    def voir_invitations(self, obj):
        url = reverse('admin_invitations', args=[obj.id])
        return format_html(f'<a href="{url}">📊 Gérer les invitations</a>')
    
    voir_invitations.short_description = "Invitations"   

# ================================
# Enregistrement du modèle Evenement
# ================================
admin.site.register(Evenement, EvenementAdmin)
