from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models.signals import post_save
# When a user is created we want to get post_save signal which gets fired after an object is saved
from django.dispatch import receiver    # a function that gets the signal and performs a specific task


# In order to tie the functionality of creating a user profile upon each new user together, user a receiver decorator:
@receiver(post_save, sender=User)   # when a user is saved, then send a signal to the receiver
# (receiver being the function below)
def create_user_profile(sender, instance, created, **kwargs):
    # The function takes all of the arguments that the post_save signal passes to it
    # The function is run every time a user is created
    # For each new user, a user profile is also automatically created
    if created:
        UserProfile.objects.create(user=instance)   # create a profile for the user


@receiver(post_save, sender=User)  # when a user is saved, then send a signal to the receiver
# (receiver being the function below)
def save_user_profile(sender, instance, **kwargs):
    # The function saves the user profile every time the user object gets saved
    instance.userprofile.save()     # save the user profile
