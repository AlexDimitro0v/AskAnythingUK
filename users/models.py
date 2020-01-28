from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class UserProfile(models.Model):
    """One-to-one relationship with the existing user model"""
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    url_link_1 = models.URLField("Personal Website Link 1", blank=True)
    url_link_2 = models.URLField("Personal Website Link 2", blank=True)
    url_link_3 = models.URLField("Personal Website Link 3", blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # the dir where the images get uploaded to
    user = models.OneToOneField(User, on_delete=models.CASCADE)   # if the user is deleted then also delete the profile
    premium_ends = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} Profile"
