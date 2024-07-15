from django.db import migrations, transaction
from django.contrib.auth.models import User
from django.utils import timezone

from advisee.models import Advisee
from advisor.models import Advisor

def populate_data(apps, schema_editor):
    advisor = Advisor.objects.get(id=1)

    u1 = User.objects.create_user(
        username="advisee1",
        email='advisee1@mailinator.com', 
        is_active=1, 
        password="advisee1", 
        first_name="advisee", 
        last_name="1", 
        last_login=timezone.now())
    
    a1 = Advisee(user=u1, advisor=advisor)
    a1.save()

    u2 = User.objects.create_user(
        username="advisee2",
        email='advisee2@mailinator.com', 
        is_active=1, 
        password="advisee2", 
        first_name="advisee", 
        last_name="2", 
        last_login=timezone.now())
    a2 = Advisee(user=u2, advisor=advisor)
    a2.save()

class Migration(migrations.Migration):
    dependencies = [
        ('advisee', '0002_advisee_advisor'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]