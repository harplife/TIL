# Generated by Django 2.2.2 on 2019-06-19 07:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0005_auto_20190619_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
