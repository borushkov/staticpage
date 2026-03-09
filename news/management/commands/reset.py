from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category  

class Command( BaseCommand):
    help = 'Стирает все новости из определенной категории'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        category_name = input('Введите название категории для удаления: ')
        self.stdout.write(f'Вы выбрали категорию: {category_name}')
        confirm = input('Вы уверены, что хотите удалить все новости из этой категории? (yes/no): ')
        if confirm.lower() == 'yes':
            try:
                category = Category.objects.get(name = options['category'])
                post_to_delete = Post.objects.filter(categories=category_name).delete
                self.stdout.write(self.style.SUCCESS(f'Все новости из категории "{category_name}" были удалены.'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {options['category']}'))


                

    
 