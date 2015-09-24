#coding: utf-8

import random

from django.core.management.base import BaseCommand, CommandError
from ranking_real_time.models import Player

import redis
cache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

class Command(BaseCommand):
    help = 'Inicia pontuação dos usuários no mysql'

    def handle(self, *args, **options):
        print 'Reiniciando pontuação'
        players =Player.objects.all()
        for player in players:
            player.pontos = 1000
            player.save()
            cache.zadd('ranking:username', 1000, player)
        print '\e[1;32mTodos os jogadores iniciados com 1000 pontos'