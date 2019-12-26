from django.contrib import admin
from .models import FeedbackRequest, Rating, Category

# Register your models here.
admin.site.register(FeedbackRequest)
admin.site.register(Rating)
# admin.site.register(Feedbacker)
admin.site.register(Category)
