from django.contrib import admin
from .models import News, Category, images, MyFavoriteNews
# Register your models here.

admin.site.register(News)
admin.site.register((Category, images, MyFavoriteNews))
