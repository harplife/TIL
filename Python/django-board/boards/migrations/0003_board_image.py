# Generated by Django 2.2.2 on 2019-06-13 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]