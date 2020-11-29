from django.contrib import admin
from .models import comment, likes, dislikes
# Register your models here.

admin.site.register((comment, likes, dislikes))