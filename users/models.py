from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class userExtraField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='user')
    dob = models.DateField()