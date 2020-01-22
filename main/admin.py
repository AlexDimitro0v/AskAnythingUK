from django.contrib import admin
from .models import FeedbackRequest, Rating, Category, FeedbackerCandidate, Area

# Register your models here.
admin.site.register(FeedbackRequest)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(FeedbackerCandidate)
admin.site.register(Area)
