from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# https://stackoverflow.com/questions/14663523/foreign-key-django-model
# https://stackoverflow.com/questions/6928692/how-to-express-a-one-to-many-relationship-in-django
# Note that ForeignKey in Django represents Many-to-One relationship !!! i.e. a feedbackee can have many requests
#
# OneToOneField represents one to one relationship
# ManyToManyField represents many to many relationship


class FeedbackRequest(models.Model):
    title = models.CharField(max_length=100)
    maintext = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(default=timezone.now)
    time_limit = models.IntegerField(default=7)
    premium = models.BooleanField(default=False)
    # Why would you delete the feedbackee when you delete a feedback request? models.CASCADE --into-> PROTECT
    feedbackee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='request_feedbackee')
    # Initially the feedbacker is set to the author (i.e. feedbackee = feedbacker)
    feedbacker = models.ForeignKey(User, on_delete=models.PROTECT, related_name='request_feedbacker')
    reward = models.IntegerField(default=0)
    feedbacker_comments = models.TextField(default="")

    def __str__(self):
        return self.title


class Rating(models.Model):
    feedbackee = models.ForeignKey(User, on_delete=models.SET("Anonymous"), related_name='rating_feedbackee')
    feedbacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_feedbacker')
    date_posted = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField()
    comment = models.TextField()


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class FeedbackerCandidate(models.Model):
    feedbacker = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(FeedbackRequest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.feedbacker} - {self.feedback}"


class Tag(models.Model):
    # Why would you delete the FeedbackRequest when you delete a tag or category? models.CASCADE --into-> PROTECT
    feedback = models.ForeignKey(FeedbackRequest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name


class Specialism(models.Model):
    feedback = models.ForeignKey(FeedbackRequest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# class Feedbacker(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)     # One-to-one relationship
#     # profile_description = models.TextField()
#
#     def __str__(self):
#         return self.user.username


class FeedbackerComments(models.Model):
    feedbacker_comments = models.TextField(default="")
