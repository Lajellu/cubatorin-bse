from django.db import migrations, transaction
from advisor.models import Topic

def populate_data(apps, schema_editor):
    print ("Deprecated. Use: python manage.py seed_db")
    # Topic.objects.create(name='Market Sizing')
    # Topic.objects.create(name='Product Market Fit')
    # Topic.objects.create(name='Valuation')
    # Topic.objects.create(name='Capitalization')
    # Topic.objects.create(name='Competitive Analysis')
    # Topic.objects.create(name='Content Marketing')
    # Topic.objects.create(name='Networking')
    # Topic.objects.create(name='Customer Journey')
    # Topic.objects.create(name='Privacy and Data Compliance')
    # Topic.objects.create(name='Customer Lifetime Value')
    # Topic.objects.create(name='SaaS Metrics')

class Migration(migrations.Migration):
    dependencies = [
        ('advisor', '0003_topic'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]