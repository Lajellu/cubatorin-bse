from django.db import migrations, transaction
from advisor.models import Advisor, Topic, Article

def populate_data(apps, schema_editor):
    print ("Deprecated. Use: python manage.py seed_db")
    # ad = Advisor.objects.get(id=1)
    # t1 = Topic.objects.get(id=1) 
    # t2 = Topic.objects.get(id=2) 
    # t3 = Topic.objects.get(id=3)

    # Article.objects.create(advisor=ad, topic=t1, name='Article on Market Sizing', status='SUCCEEDED')
    # Article.objects.create(advisor=ad, topic=t2, name='Article on Product Market Fit', status='SUCCEEDED')
    # Article.objects.create(advisor=ad, topic=t3, name='Article on Valuation', status='SUCCEEDED')
    


class Migration(migrations.Migration):
    dependencies = [
        ('advisor', '0007_article_body_article_failure_reason_article_status'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]