from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from django.utils import timezone

class Advisor(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Topic(Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Article(Model):
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    uploaded_on = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "Article: '" + self.name + "' about '" + topic.name + "' Uploaded on " + uploaded_on