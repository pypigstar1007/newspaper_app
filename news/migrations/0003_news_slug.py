# Generated by Django 3.1.3 on 2020-11-28 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20201128_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]