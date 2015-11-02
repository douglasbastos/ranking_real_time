#coding: utf-8

from django.core.management.base import BaseCommand
from ranking_real_time.models import Player
from django.conf import settings

import redis
cache = redis.StrictRedis(host=settings.REDIS_DB['host'],
                          port=settings.REDIS_DB['port'],
                          db=settings.REDIS_DB['db'])


class Command(BaseCommand):
    help = 'Inicia pontuação dos usuários no mysql'

    def handle(self, *args, **options):
        print 'Reiniciando pontuação'
        players = Player.objects.all()
        for player in players:
            player.pontos = 1000
            player.save()
            cache.zadd('ranking:username', 1000, player)
        print 'Todos os jogadores iniciados com 1000 pontos'
