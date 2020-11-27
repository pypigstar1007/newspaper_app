from django.db import models
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
    return '{0}/{1}/{2}.png'.format(instance.image_for.created_by, instance.image_for.id, filename)
# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255, default='')
    news_body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)


class images(models.Model):
    image_for = models.ForeignKey(News, on_delete=models.CASCADE)
    imgage = models.ImageField(upload_to=get_upload_path)