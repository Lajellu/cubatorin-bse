from django.db import migrations, transaction
from django.contrib.auth.models import User
from django.utils import timezone

from advisee.models import Advisee
from advisor.models import Advisor

def populate_data(apps, schema_editor):
    print ("Migration deprecated. Will seed at the end of all migrations. ")
    # ad1 = Advisee.objects.get(id=1)
    # ad1.market_sizing =                 "ad1 market sizing"
    # ad1.product_market_fit =            "ad1 product market fit"
    # ad1.valuation =                     "ad1 valuation"
    # ad1.capitalization =                "ad1 capitalization"
    # ad1.competitive_analysis =          "ad1 competitive analysis"
    # ad1.content_marketing =             "ad1 content marketing"
    # ad1.networking =                    "ad1 networking"
    # ad1.customer_journey =              "ad1 customer journey"
    # ad1.privacy_and_data_compliance =   "ad1 privacy and data compliance"
    # ad1.customer_lifetime_value =       "ad1 customer lifetime value"
    # ad1.saas_metrics =                  "ad1 saas metrics"
    # ad1.save()

    # ad2 = Advisee.objects.get(id=2)
    # ad2.market_sizing =                 "ad2 market sizing"
    # ad2.product_market_fit =            "ad2 product market fit"
    # ad2.valuation =                     "ad2 valuation"
    # ad2.capitalization =                "ad2 capitalization"
    # ad2.competitive_analysis =          "ad2 competitive analysis"
    # ad2.content_marketing =             "ad2 content marketing"
    # ad2.networking =                    "ad2 networking"
    # ad2.customer_journey =              "ad2 customer journey"
    # ad2.privacy_and_data_compliance =   "ad2 privacy and data compliance"
    # ad2.customer_lifetime_value =       "ad2 customer lifetime value"
    # ad2.saas_metrics =                  "ad2 saas metrics"
    # ad2.save()

class Migration(migrations.Migration):
    dependencies = [
        ('advisee', '0004_advisee_capitalization_advisee_competitive_analysis_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]