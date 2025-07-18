from django.urls import path
from . import views

urlpatterns = [
    path('invitation/<int:invitation_id>/', views.afficher_et_repondre_invitation, name='afficher_invitation'),
    path('admin-invitations/<int:evenement_id>/', views.vue_liste_invitations, name='admin_invitations'),
    path('',views.login_vue, name='login_vue'),
    path('evenement/', views.cree_evenement, name='cree_evenement'),
    path('evenement/<int:evenement_id>/invitations/', views.gestion_invitations, name='gestion_invitations'),
    path('accueil/', views.accueil_vue, name='accueil_vue'),
    path('accueil/gestion_invitations', views.gestion_invitations, name='gestion_invitations'),
    path('evenement/<int:evenement_id>/creer-invitation/', views.cree_invitation, name='cree_invitation'),
    path('evenement/<int:evenement_id>/supprimer/', views.supprimer_evenement, name='supprimer_evenement'),
    path('invitation/<int:invitation_id>/supprimer/', views.supprimer_invitation, name='supprimer_invitation'),
    path('inscription/', views.inscription_vue, name='inscription_vue'),
    path('deconnexion/', views.deconnexion_vue, name='deconnexion_vue'),
    path('evenement/<int:evenement_id>/invitations/actions/', views.action_invitations_groupees, name='action_invitations_groupees'),
    

]
