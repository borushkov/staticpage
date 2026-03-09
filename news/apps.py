from django.apps import AppConfig
import redis

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals
red = redis.Redis(
    host = 'redis-16982.c73.us-east-1-2.ec2.cloud.redislabs.com',
    port = 16982,
    password = '5uXCDmoVQAZxbsHiIzQcRK71xxWqz8nJ'
)
