from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from celery.schedules import crontab
#6378
@shared_task
def send_post_notification(post_id):
    from .models import Post, Category
    post = Post.objects.get(id = post_id)
    emails = set()
    for category in post.categories.all():
        for user in category.subscribers.all():
            emails.add(user.email)

    send_mail(
        subject = f'Новая новость : {post.title}', 
        message = post.text[:500], 
        from_email = None, 
        recipient_list = list(emails), 
    )

@shared_task
def hello():
    return "Hello from Celery"

