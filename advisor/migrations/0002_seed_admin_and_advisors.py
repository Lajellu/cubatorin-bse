from django.db import migrations, transaction
from django.contrib.auth.models import User
from advisor.models import Advisor
from django.utils import timezone

def populate_data(apps, schema_editor):
    su = User.objects.create_superuser(
        username='admin', 
        email='admin@mailinator.com', 
        password='admin', 
        first_name="Laily", 
        last_name="Ajellu",
        last_login=timezone.now())

    # su = User(username="admin", is_active=1, is_staff=1, is_superuser=1, password="admin", , last_login=timezone.now())
    # su.save()

    u1 = User.objects.create_user(
        username="advisor1",
        email='advisor1@mailinator.com', 
        is_active=1, 
        password="advisor1", 
        first_name="advisor", 
        last_name="1", 
        last_login=timezone.now())
    a1 = Advisor(user=u1)
    a1.save()

    u2 = User.objects.create_user(
        username="advisor2",
        email='advisor2@mailinator.com', 
        is_active=1, 
        password="advisor2", 
        first_name="advisor", 
        last_name="2", 
        last_login=timezone.now())
    a2 = Advisor(user=u2)
    a2.save()

class Migration(migrations.Migration):
    dependencies = [
        ('advisor', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]