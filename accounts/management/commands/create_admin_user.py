from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create an admin user for the Interview IQ platform'

    def handle(self, *args, **options):
        username = input('Admin username: ').strip()
        email = input('Admin email: ').strip()
        password = input('Admin password: ').strip()

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User "{username}" already exists.'))
            return

        user = User.objects.create(
            username=username,
            email=email,
            user_type='admin',
            is_staff=True,
        )
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created successfully!'))
