from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from django.utils import timezone

class Advisor(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Advisor({self.id}:{self.user.username})"

class Topic(Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Topic({self.id}:{self.name})"
        # return "Topic(" + self.id + ": " + self.name + ")"

class Article(Model):
    STATUS_CHOICES = [
        ('PROCESSING', 'Processing'),
        ('FAILED', 'Failed'),
        ('SUCCEEDED', 'Succeeded'),
    ]

    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    uploaded_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PROCESSING')
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=False, null=False, default='')

    def __str__(self):
        return f"Article({self.id}:{self.name} -on- {self.topic.name})"