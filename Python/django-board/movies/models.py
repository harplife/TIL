from django.db import models

# Create your models here.


class movie(models.Model):
    title = models.CharField(max_length=100)
    title_origin = models.CharField(max_length=100)
    vote_count = models.IntegerField()
    open_date = models.CharField(max_length=30)
    genre = models.CharField(max_length=20)
    score = models.FloatField()
    poster_url = models.TextField()
    description = models.TextField()