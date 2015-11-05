# coding: utf-8
import time
from random import choice
from django.core.management.base import BaseCommand
from ranking_real_time.models import Player
from django.conf import settings

import redis
cache = redis.StrictRedis(host=settings.REDIS_DB['host'],
                          port=settings.REDIS_DB['port'],
                          db=settings.REDIS_DB['db'])


class Command(BaseCommand):
    help = 'Insere pontos dos usuários no mysql'

    def add_arguments(self, parser):
        parser.add_argument('-t', dest='time',
                            default=30, help='Set time script to run')

    def jogar_partida(self, pontos):
        result = choice(('winner', 'loser'))
        pontos_ganhos = 25 if result == 'winner' else -25
        if pontos > 25 or result == 'winner':
            pontos += pontos_ganhos
        else:
            pontos = 0
        return pontos

    def handle(self, *args, **options):
        players = Player.objects.all()
        start = now = time.time()
        duration = int(options['time'])
        limit = start + duration
        while now <= limit:
            player_sorteado = choice(players)
            player_sorteado.pontos = self.jogar_partida(player_sorteado.pontos)
            player_sorteado.save()
            cache.zadd('ranking:username', player_sorteado.pontos, player_sorteado.username)
            now = time.time()
            print 'Jogador {} está com {} pontos'.format(player_sorteado.username, player_sorteado.pontos)
