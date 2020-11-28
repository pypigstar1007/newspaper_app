# Generated by Django 3.1.3 on 2020-11-27 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('comment_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]