#coding: utf-8

import random

from django.core.management.base import BaseCommand, CommandError
from ranking_real_time.models import Player

import redis
cache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

class Command(BaseCommand):
    help = 'Insere pontos dos usuários no mysql'

    def jogar_partida(self, pontos):
        result = random.randint(0, 1)
        # result == 1 == vitória + 25 pontos
        # result == 0 == derrota - 25 pontos 
        pontos_da_partida = 25 if result == 1 else -25
        if pontos > 25 or result == 1:
            pontos += pontos_da_partida
        else:
            pontos = 0
        return pontos

    def handle(self, *args, **options):
        players =Player.objects.all()
        while True:
            player_sorteado = random.choice(players)
            player_sorteado.pontos = self.jogar_partida(player_sorteado.pontos)
            player_sorteado.save()
            cache.zadd('ranking:username', player_sorteado.pontos, player_sorteado.username)
            print 'Jogador {} está com {} pontos'.format(player_sorteado.username, player_sorteado.pontos)