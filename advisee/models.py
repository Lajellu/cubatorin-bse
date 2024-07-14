from django.contrib.auth.models import User
from django.db import models

from advisor.models import Advisor

class Advisee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, null=True, on_delete=models.SET_NULL)
