from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FeedbackRequest(models.Model):
    title = models.CharField(max_length = 100)
    maintext = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    premium = models.BooleanField(default=False)
    feedbackee = models.ForeignKey(User,on_delete=models.CASCADE)
