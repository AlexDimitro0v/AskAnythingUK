from django.contrib import admin
from .models import UserProfile, Specialism

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Specialism)