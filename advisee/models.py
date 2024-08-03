from django.contrib.auth.models import User
from django.db import models

from advisor.models import Advisor

class Advisee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, null=True, on_delete=models.SET_NULL)

    industry = models.TextField(blank=True, null=False, default='')

    biz_plan = models.TextField(blank=True, null=False, default='')

    market_sizing = models.TextField(blank=True, null=False, default='')
    product_market_fit = models.TextField(blank=True, null=False, default='')
    valuation = models.TextField(blank=True, null=False, default='')
    capitalization = models.TextField(blank=True, null=False, default='')
    competitive_analysis = models.TextField(blank=True, null=False, default='')
    content_marketing = models.TextField(blank=True, null=False, default='')
    networking = models.TextField(blank=True, null=False, default='')
    customer_journey = models.TextField(blank=True, null=False, default='')
    privacy_and_data_compliance = models.TextField(blank=True, null=False, default='')
    customer_lifetime_value = models.TextField(blank=True, null=False, default='')
    saas_metrics = models.TextField(blank=True, null=False, default='')

    @staticmethod
    def get_topics_dict():
        return {
            'market_sizing': 'Market Sizing',
            'product_market_fit': 'Product Market Fit',
            'valuation': 'Valuation',
            'capitalization' : 'Capitalization',
            'competitive_analysis': 'Competitive Analysis',
            'content_marketing': 'Content Marketing',
            'networking': 'Networking',
            'customer_journey': 'Customer Journey',
            'privacy_and_data_compliance': 'Privacy and Data Compliance',
            'customer_lifetime_value': 'Customer Lifetime Value',
            'saas_metrics': 'SaaS Metrics',
        }