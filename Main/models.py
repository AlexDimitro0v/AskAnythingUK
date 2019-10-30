from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FeedbackRequest(models.Model):
    title = models.CharField(max_length = 100)
    maintext = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(default=timezone.now)
    time_limit = models.IntegerField(default=7)
    premium = models.BooleanField(default=False)
    feedbackee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_feedbackee')
    feedbacker = models.ForeignKey(User,on_delete=models.PROTECT,related_name='request_feedbacker')
    reward = models.IntegerField(default=0)

class Rating(models.Model):
    feedbackee = models.ForeignKey(User,on_delete=models.SET("Anonymous"),related_name='rating_feedbackee')
    feedbacker = models.ForeignKey(User, on_delete=models.CASCADE,related_name='rating_feedbacker')
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField()
    comment = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length = 32)

class FeedbackerCandidate(models.Model):
    feedbacker = models.ForeignKey(User,on_delete=models.CASCADE)
    feedback = models.ForeignKey(FeedbackRequest,on_delete=models.CASCADE)

class Tag(models.Model):
    feedback = models.ForeignKey(FeedbackRequest,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Specialism(models.Model):
    feedback = models.ForeignKey(FeedbackRequest,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Feedbacker(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_description = models.TextField()
