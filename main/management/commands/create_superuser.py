from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config


class Command(BaseCommand):
    help = 'Create a superuser with environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = config('ADMIN_USERNAME', default='admin')
        email = config('ADMIN_EMAIL', default='admin@example.com')
        password = config('ADMIN_PASSWORD', default='admin123')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
            return
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{username}" created successfully!')
        )
        self.stdout.write(
            self.style.WARNING('Please change the default password after first login.')
        )