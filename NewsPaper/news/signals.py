from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import send_post_notification

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        send_post_notification.delay(instance.id)