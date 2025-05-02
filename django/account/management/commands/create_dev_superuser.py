import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import FamilyGroup

class Command(BaseCommand):
    help = 'Create a default superuser and family group for dev environments.'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "password")
        family_name = os.getenv("DJANGO_SUPERUSER_FAMILY", "開発")
        group_password = os.getenv("DJANGO_SUPERUSER_FAMILY_PASSWORD", "family_password")
        name = os.getenv("DJANGO_SUPERUSER_NAME", "Admin")

        if not FamilyGroup.objects.filter(name=family_name).exists():
            family = FamilyGroup.objects.create(name=family_name, secret_key=group_password)
            self.stdout.write(self.style.SUCCESS(f"FamilyGroup created: {family_name}"))
        else:
            family = FamilyGroup.objects.get(name=family_name)
            self.stdout.write(self.style.WARNING(f"FamilyGroup already exists: {family_name}"))

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password, familygroup=family, name=name)
            self.stdout.write(self.style.SUCCESS(f"Superuser created: {email}"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser already exists: {email}"))