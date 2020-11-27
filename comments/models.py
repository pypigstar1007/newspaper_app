from django.db import models
from news.models import News
from django.contrib.auth.models import User
# Create your models here.

class comment(models.Model):
    comment_for = models.ForeignKey(News, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    likes = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)