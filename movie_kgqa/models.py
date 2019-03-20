# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    actor_bio = models.TextField(blank=True, null=True)
    actor_chname = models.CharField(db_column='actor_chName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actor_forename = models.CharField(db_column='actor_foreName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actor_nationality = models.CharField(max_length=100, blank=True, null=True)
    actor_constellation = models.CharField(max_length=100, blank=True, null=True)
    actor_birthplace = models.CharField(db_column='actor_birthPlace', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actor_birthday = models.CharField(db_column='actor_birthDay', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actor_repworks = models.CharField(db_column='actor_repWorks', max_length=100, blank=True, null=True)  # Field name made lowercase.
    actor_achiem = models.TextField(blank=True, null=True)
    actor_brokerage = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'actor'


class ActorToMovie(models.Model):
    actor_id = models.IntegerField()
    movie_id = models.IntegerField()
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'actor_to_movie'


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'genre'


class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    movie_bio = models.TextField(blank=True, null=True)
    movie_chname = models.CharField(db_column='movie_chName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    movie_forename = models.CharField(db_column='movie_foreName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    movie_prodtime = models.CharField(db_column='movie_prodTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    movie_prodcompany = models.CharField(db_column='movie_prodCompany', max_length=100, blank=True, null=True)  # Field name made lowercase.
    movie_director = models.CharField(max_length=100, blank=True, null=True)
    movie_screenwriter = models.CharField(max_length=100, blank=True, null=True)
    movie_genre = models.CharField(max_length=100, blank=True, null=True)
    movie_star = models.CharField(max_length=100, blank=True, null=True)
    movie_length = models.CharField(max_length=100, blank=True, null=True)
    movie_releasetime = models.CharField(db_column='movie_releaseTime', max_length=100, blank=True, null=True)  # Field name made lowercase.
    movie_language = models.CharField(max_length=100, blank=True, null=True)
    movie_achiem = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movie'


class MovieToGenre(models.Model):
    movie_id = models.IntegerField()
    genre_id = models.IntegerField()
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'movie_to_genre'
