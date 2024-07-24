from django.db import migrations, transaction
from advisor.models import Advisor, Topic, Article

def populate_data(apps, schema_editor):
    print ("Migration deprecated. Will seed at the end of all migrations. ")
    # ad = Advisor.objects.get(id=1)
    # t1 = Topic.objects.get(id=1) 
    # t2 = Topic.objects.get(id=2) 
    # t3 = Topic.objects.get(id=3)

    # Article.objects.create(advisor=ad, topic=t1, name='Article on Market Sizing')
    # Article.objects.create(advisor=ad, topic=t2, name='Article on Product Market Fit')
    # Article.objects.create(advisor=ad, topic=t3, name='Article on Valuation')
    


class Migration(migrations.Migration):
    dependencies = [
        ('advisor', '0005_article'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]