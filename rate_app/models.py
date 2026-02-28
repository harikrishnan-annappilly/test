from django.db import models

# Create your models here.


class Tbl_User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    allowed = models.BooleanField(default=False)


class Tbl_Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    genre = models.CharField(max_length=30)
    rating = models.FloatField()
    year = models.IntegerField()


class Tbl_Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Tbl_User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Tbl_Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=100)
