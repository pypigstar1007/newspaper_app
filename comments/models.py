from django.db import models
from news.models import News
from django.contrib.auth.models import User
# Create your models here.

class comment(models.Model):
    comment_for = models.ForeignKey(News, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)


class likes(models.Model):
    for_news = models.ForeignKey(News, on_delete=models.CASCADE)
    like_by = models.ManyToManyField(User, related_name='like_user')


class dislikes(models.Model):
    for_news = models.ForeignKey(News, on_delete=models.CASCADE)
    dislike_by = models.ManyToManyField(User, related_name='dislike_user')
