from django.db import migrations, transaction
from django.contrib.auth.models import User
from django.utils import timezone

from advisee.models import Advisee
from advisor.models import Advisor

def populate_data(apps, schema_editor):
    print ("Deprecated. Use: python manage.py seed_db")
    # advisor = Advisor.objects.get(id=1)

    # u1 = User.objects.create_user(
    #     username="advisee1",
    #     email='advisee1@mailinator.com', 
    #     is_active=1, 
    #     password="advisee1", 
    #     first_name="advisee", 
    #     last_name="1",
    #     last_login=timezone.now()
    #     )
    
    # a1 = Advisee(
    #     user=u1, 
    #     advisor=advisor,
    #     industry =                      "ad1 industry",
    #     market_sizing =                 "ad1 market sizing",
    #     product_market_fit =            "ad1 product market fit",
    #     valuation =                     "ad1 valuation",
    #     capitalization =                "ad1 capitalization",
    #     competitive_analysis =          "ad1 competitive analysis",
    #     content_marketing =             "ad1 content marketing",
    #     networking =                    "ad1 networking",
    #     customer_journey =              "ad1 customer journey",
    #     privacy_and_data_compliance =   "ad1 privacy and data compliance",
    #     customer_lifetime_value =       "ad1 customer lifetime value",
    #     saas_metrics =                  "ad1 saas metrics",
    #     )
    # a1.save()

    # u2 = User.objects.create_user(
    #     username="advisee2",
    #     email='advisee2@mailinator.com', 
    #     is_active=1, 
    #     password="advisee2", 
    #     first_name="advisee", 
    #     last_name="2", 
    #     last_login=timezone.now()
    #     )

    # a2 = Advisee(
    #     user=u2, 
    #     advisor=advisor,
    #     industry =                      "ad2 industry",
    #     market_sizing =                 "ad2 market sizing",
    #     product_market_fit =            "ad2 product market fit",
    #     valuation =                     "ad2 valuation",
    #     capitalization =                "ad2 capitalization",
    #     competitive_analysis =          "ad2 competitive analysis",
    #     content_marketing =             "ad2 content marketing",
    #     networking =                    "ad2 networking",
    #     customer_journey =              "ad2 customer journey",
    #     privacy_and_data_compliance =   "ad2 privacy and data compliance",
    #     customer_lifetime_value =       "ad2 customer lifetime value",
    #     saas_metrics =                  "ad2 saas metrics",

    #     )
    # a2.save()

class Migration(migrations.Migration):
    dependencies = [
        ('advisee', '0006_advisee_industry'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]