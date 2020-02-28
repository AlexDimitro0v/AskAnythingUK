from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import Category
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class UserProfile(models.Model):
    """One-to-one relationship with the existing user model"""
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    phone_number = PhoneNumberField(null=True)
    dob = models.DateField(null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    messages_notifications = models.BooleanField(default=True)
    feedback_updates_notifications = models.BooleanField(default=True)
    smart_recommendations_notifications = models.BooleanField(default=True)
    messages_mail_notifications = models.BooleanField(default=True)
    smart_recommendations_mail_notifications = models.BooleanField(default=True)
    payment_method = models.BooleanField(default=False)
    linkedin = models.URLField("LinkedIn", blank=True)
    url_link_1 = models.URLField("Personal Website Link 1", blank=True)
    url_link_2 = models.URLField("Personal Website Link 2", blank=True)
    url_link_3 = models.URLField("Personal Website Link 3", blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # the dir where the images get uploaded to
    user = models.OneToOneField(User, on_delete=models.CASCADE)   # if the user is deleted then also delete the profile
    premium_ends = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(default=False)
    most_common_words = ArrayField(
            models.CharField(max_length=30, blank=True),
            size=30,
            default=list()
        )
    most_common_words_numbers = ArrayField(
                models.IntegerField(default=0),
                size=30,
                default=list()
            )
            
    def __str__(self):
        return f"{self.user.username} Profile"


class Specialism(models.Model):
    feedbacker = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.feedbacker} - {self.category}"
