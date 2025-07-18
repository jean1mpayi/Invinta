from django import forms
from .models import Evenement, Invitation
from django.contrib.auth.models import User

# ───────────────────────────────────────────────────────────────
# Formulaire pour inviter un utilisateur à un événement
# ───────────────────────────────────────────────────────────────
class InvitationForm(forms.ModelForm):
    """
    Permet à un organisateur de renseigner les informations de l'invité :
    nom, email et statut de l'invitation.
    """
    class Meta:
        model = Invitation
        fields = ['nom_invite', 'email', 'statut']
        widgets = {
            'nom_invite': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black'}),
            'statut': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black'}),
        }

# ───────────────────────────────────────────────────────────────
# Formulaire pour créer/modifier un événement
# ───────────────────────────────────────────────────────────────
class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'date', 'lieu', 'description', 'style_invitation', 'image_evenement']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-white/80 text-black',
                'placeholder': 'Titre de l\'événement'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'w-full p-2 rounded bg-white/80 text-black',
                'type': 'datetime-local'
            }),
            'lieu': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-white/80 text-black',
                'placeholder': 'Lieu'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded bg-white/80 text-black',
                'placeholder': 'Description',
                'rows': 3
            }),
            'style_invitation': forms.Select(attrs={
                'class': 'w-full p-2 rounded bg-white/80 text-black'
            }),
        }

   


# ───────────────────────────────────────────────────────────────
# Formulaire d'inscription utilisateur
# ───────────────────────────────────────────────────────────────
class InscriptionForm(forms.ModelForm):
    """
    Formulaire d'inscription avec confirmation de mot de passe.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black'
    }), label="Mot de passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black'
    }), label="Confirmer le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black'}),
        }
        help_texts = {
            'username': None,
        }

    def clean(self):
        """
        Valide que les mots de passe sont identiques.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas.")
        return cleaned_data

# ───────────────────────────────────────────────────────────────
# Formulaire de connexion
# ───────────────────────────────────────────────────────────────
class LoginForm(forms.Form):
    """
    Formulaire de connexion simple.
    """
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black',
            'placeholder': "Nom d'utilisateur"
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 rounded border border-gray-300 text-black',
            'placeholder': "Mot de passe"
        })
    )
