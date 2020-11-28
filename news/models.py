from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime

def get_upload_path(instance, filename):
    return '{0}/{1}/{2}.png'.format(instance.image_for.created_by, instance.image_for.id, filename)




class Category(models.Model):
    Category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.Category_name

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255, default='') # this is the detaild title/ heading of the news
    headline = models.CharField(max_length=50, default='') # this will be use in the front of home page
    news_body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def get_body(self):
        texts = self.news_body
        returned_text = str(texts)[ :100]
        print(returned_text)
        if len(texts) > 100:
            return returned_text + '...'
        else:
            return texts

    @property
    def get_heading(self):
        headings = self.headline
        if headings == '':
            headings = self.title
            return headings[: 10]
        return headings

    @property
    def uploaded_from_now(self):
        timedeff = datetime.now() - self.created_at
        return timedeff.second()

class images(models.Model):
    image_for = models.ForeignKey(News, on_delete=models.CASCADE)
    imgage = models.ImageField(upload_to=get_upload_path)
