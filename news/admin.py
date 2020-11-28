from django.contrib import admin
from .models import News, Category, images
# Register your models here.

admin.site.register(News)
admin.site.register((Category, images))
