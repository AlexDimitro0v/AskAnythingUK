from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    """One-to-one relationship with the existing user model"""
    city = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # the dir where the images get uploaded to
    user = models.OneToOneField(User, on_delete=models.CASCADE)   # if the user is deleted then also delete the profile
    # One-to-one relationship is appropriate here instead of a ForeignKey (many to one relationship)
    # https://stackoverflow.com/questions/54182179/how-to-display-the-user-avatar-on-all-templates-django-i-use-base-html

    def __str__(self):
        return f"{self.user.username} Profile"

