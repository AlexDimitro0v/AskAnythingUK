from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# https://stackoverflow.com/questions/14663523/foreign-key-django-model
# https://stackoverflow.com/questions/6928692/how-to-express-a-one-to-many-relationship-in-django
# Note that ForeignKey in Django represents Many-to-One relationship !!! i.e. a feedbackee can have many requests
# OneToOneField represents one to one relationship
# ManyToManyField represents many to many relationship


class Area(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class FeedbackRequest(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    maintext = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_started = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(default=timezone.now)
    time_limit = models.IntegerField(default=7)
    premium = models.BooleanField(default=False)
    # If feedbackee(the one who posts the request) is deleted, delete the feedback request instance (do we want this?)
    feedbackee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_feedbackee')
    # Initially the feedbacker is set to the author (i.e. feedbackee = feedbacker)
    # Cannot delete a feedbacker of an existing request!
    feedbacker = models.ForeignKey(User, on_delete=models.PROTECT, related_name='request_feedbacker')
    reward = models.IntegerField(default=0)
    feedbacker_comments = models.TextField(default="")
    feedbacker_rated = models.IntegerField(default=False)

    def __str__(self):
        return self.title


class Rating(models.Model):
    feedbackee = models.ForeignKey(User, on_delete=models.SET("Anonymous"), related_name='rating_feedbackee')
    feedbacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_feedbacker')
    date_posted = models.DateTimeField(default=timezone.now)
    quality = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    communication = models.IntegerField(default=0)
    review = models.TextField(default="")

    def __str__(self):
        return f"{self.feedbackee}-{self.feedbacker} Review"


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class FeedbackerCandidate(models.Model):
    feedbacker = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(FeedbackRequest, on_delete=models.CASCADE)
    application = models.CharField(max_length=300,default="")

    def __str__(self):
        return f"{self.feedbacker} - {self.feedback}"


class Tag(models.Model):
    feedback = models.ForeignKey(FeedbackRequest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name


# Why do we need this lonely model when we have feedbacker_comments field in the FeedbackRequest Model?
class FeedbackerComments(models.Model):
    feedbacker_comments = models.TextField(default="")


class Purchase(models.Model):
    # Cannot delete a feedback of an existing purchase!
    feedback = models.ForeignKey(FeedbackRequest, on_delete=models.PROTECT)
    # Cannot delete a feedbackee of an existing purchase!
    feedbackee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='buyer')
    feedbacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    time = models.DateTimeField(default=timezone.now)
    is_completed = models.IntegerField(default=False)

    def __str__(self):
        return f"{self.feedback.title} Purchase"
