# coding: utf-8

from django.db import models
from django.contrib.auth.models import User 


class Player(models.Model):
    username = models.ForeignKey(User)
    pontos = models.IntegerField()