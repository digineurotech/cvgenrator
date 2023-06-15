from django.contrib import admin
from .models import Profile
# Register your models here.
admin.site.site_title = "CV Genrator"
admin.site.site_header = "CV Genrator"
admin.site.register(Profile)
