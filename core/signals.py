from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Invitation

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# ...

@receiver(post_save, sender=Invitation)
def envoyer_email_confirmation(sender, instance, created, **kwargs):
    if not created:
        if instance.statut == 'accepte':
            sujet = "🎉 Confirmation de votre invitation"
            template = 'emails/confirmation.html'
        elif instance.statut == 'refuse':
            sujet = "❌ Refus de votre invitation"
            template = 'emails/refus.html'
        else:
            return

        context = {'invitation': instance}

        message_html = render_to_string(template, context)
        message_txt = strip_tags(message_html)

        send_mail(
            sujet,
            message_txt,
            None,
            [instance.email],
            html_message=message_html,
            fail_silently=True
        )

