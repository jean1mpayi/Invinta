from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import EvenementForm, InvitationForm
from .models import Invitation, Evenement
from .forms import InscriptionForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import LoginForm
from django.contrib import messages
import csv
from django.views.decorators.http import require_POST
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO



# 🔹 Vue publique : affichage et réponse à une invitation
def afficher_et_repondre_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    message = None

    # Récupération de la réponse transmise dans l'URL
    reponse = request.GET.get("reponse")

    # Vérifier si l'utilisateur connecté est le créateur de l'événement
    evenement = invitation.evenement
    est_createur = request.user.is_authenticated and request.user == evenement.organisateur

    # Si une réponse est fournie, mettre à jour le statut
    if reponse in ["accepte", "refuse"]:
        invitation.statut = reponse
        invitation.save()
        if reponse == "accepte":
            message = "✅ Merci d’avoir accepté l’invitation."
        else:
            message = "❌ Vous avez refusé l’invitation."

    # Affichage de la page (avec ou sans réponse)
    return render(request, "core/invitation.html", {
        "invitation": invitation,
        "evenement": evenement,
        "message": message,
        "est_createur": est_createur
        
    })


def vue_liste_invitations(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    statut = request.GET.get('statut')
    invitations = Invitation.objects.filter(evenement=evenement)
    if statut:
        invitations = invitations.filter(statut=statut)
    # Calcul du résumé
    resume = {
        'accepte': invitations.filter(statut='accepte').count(),
        'refuse': invitations.filter(statut='refuse').count(),
        'en_attente': invitations.filter(statut='en_attente').count(),
    }
    
    return render(request, 'core/liste_invitations.html', {
        'evenement': evenement,
        'invitations': invitations,
        'resume': resume,
    })


# vue login
def login_vue(request):
    form = LoginForm(request.POST or None)
    erreur = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil_vue')
        else:
            erreur = "Identifiants invalides"
    return render(request, 'core/login.html', {"form": form, "erreur": erreur})






def accueil_vue(request):
    if request.user.is_authenticated:
        evenements = Evenement.objects.filter(organisateur=request.user)
    else:
        evenements = []
    return render(request, 'core/accueil.html', {'evenements': evenements})



@login_required
def gestion_invitations(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    invitations = Invitation.objects.filter(evenement=evenement)

    # Recherche et filtrage
    query = request.GET.get('q')
    if query:
        invitations = invitations.filter(nom_invite__icontains=query)

    statut = request.GET.get('statut')
    if statut in ['accepte', 'refuse', 'en_attente']:
        invitations = invitations.filter(statut=statut)

    # Export PDF
    if 'export_pdf' in request.GET:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Titre
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 50, f"Invitations pour l'événement : {evenement.titre}")

        # Préparer les données du tableau
        data = [['','Nom', 'Email', 'Statut']]
        for idx, inv in enumerate(invitations):
            statut_display = {
                'accepte': 'Acceptée',
                'refuse': 'Refusée',
                'en_attente': 'En attente'
            }.get(inv.statut, 'Inconnu')
            data.append([inv.nom_invite, inv.email, statut_display])


        # Créer le tableau
        table = Table(data, colWidths=[150, 200, 100])
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        table.setStyle(style)

        # Calculer position pour centrer le tableau verticalement
        table_width, table_height = table.wrap(0, 0)
        x = 50
        y = height - 100 - table_height

        table.drawOn(p, x, y)

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invitations_{evenement_id}.pdf"'
        return response

    # Stats
    total = invitations.count()
    nb_accepte = invitations.filter(statut="accepte").count()
    nb_refuse = invitations.filter(statut="refuse").count()
    nb_attente = invitations.filter(statut="en_attente").count()

    context = {
        'evenement': evenement,
        'invitations': invitations,
        'total': total,
        'nb_accepte': nb_accepte,
        'nb_refuse': nb_refuse,
        'nb_attente': nb_attente,
    }
    return render(request, 'core/gestion_invitations.html', context)




@login_required(login_url='login')
def cree_evenement(request):
    if request.method == "POST":
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.organisateur = request.user  # Associe l'utilisateur connecté
            evenement.save()
            return redirect('accueil_vue')  # Redirige vers l'accueil après création
    else:
        form = EvenementForm()
    return render(request, 'core/evenement.html', {'form': form})

@login_required(login_url='login')
def cree_invitation(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    form = InvitationForm(request.POST or None)
    invitations = Invitation.objects.filter(evenement=evenement)
    if request.method == "POST":
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.evenement = evenement
            if request.POST.get("action") == "preview":
                # Afficher l'aperçu sans sauvegarder
                return render(request, "core/preview_invitation.html", {
                    "invitation": invitation,
                    "evenement": evenement,
                    "est_createur": True,  # ou False selon le contexte
                })
            else:
                invitation.save()
                total = invitations.count()
                nb_accepte = invitations.filter(statut="accepte").count()
                nb_refuse = invitations.filter(statut="refuse").count()
                nb_attente = invitations.filter(statut="en_attente").count()

                context = {
                    'evenement': evenement,
                    'invitations': invitations,
                    'total': total,
                    'nb_accepte': nb_accepte,
                    'nb_refuse': nb_refuse,
                    'nb_attente': nb_attente,
                }
                return render(request, "core/gestion_invitations.html", context)
    return render(request, "core/cree_invitation.html", {"form": form, "evenement": evenement})



@login_required(login_url='login')
def supprimer_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id, organisateur=request.user)
    evenement.delete()
    return redirect('accueil_vue')

@login_required(login_url='login')
def supprimer_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, evenement__organisateur=request.user)
    evenement_id = invitation.evenement.id
    invitation.delete()
    return redirect('gestion_invitations', evenement_id=evenement_id)

def inscription_vue(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('login_vue')
    else:
        form = InscriptionForm()
    return render(request, 'core/inscription.html', {'form': form})



@require_POST
def action_invitations_groupees(request, evenement_id):
    ids = request.POST.getlist('selection')
    action = request.POST.get('action')

    if not ids or not action:
        messages.error(request, "Veuillez sélectionner des invitations et une action.")
        return redirect('gestion_invitations', evenement_id=evenement_id)

    invitations = Invitation.objects.filter(id__in=ids, evenement_id=evenement_id)

    if action == 'accepte':
        invitations.update(statut='accepte')
        messages.success(request, "Invitations marquées comme acceptées.")
    elif action == 'refuse':
        invitations.update(statut='refuse')
        messages.success(request, "Invitations marquées comme refusées.")
    elif action == 'supprimer':
        invitations.delete()
        messages.success(request, "Invitations supprimées.")
    else:
        messages.error(request, "Action non valide.")

    return redirect('gestion_invitations', evenement_id=evenement_id)



def deconnexion_vue(request):
    logout(request)
    return redirect('login_vue')



from django.shortcuts import render
from .models import Invitation
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    total = Invitation.objects.count()
    pending = Invitation.objects.filter(statut='en_attente').count()
    sent = Invitation.objects.filter(statut='accepte').count()

    # Exemple fictif pour le graphique : nombre d'invitations acceptées par jour
    weekly_data = [3, 5, 2, 6, 1, 4, 0]  # à remplacer plus tard par de vraies stats

    render(request, "mon_app/dashboard.html", {...}) ({
        "total_invitations": total,
        "pending_invitations": pending,
        "sent_invitations": sent,
        "weekly_data": weekly_data
    })

