from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Note
from telegram_bot import send_note_to_channel


@receiver(post_save, sender=Note)
def send_note_after_create(sender, instance, created, **kwargs):
    if created:
        send_note_to_channel(instance)