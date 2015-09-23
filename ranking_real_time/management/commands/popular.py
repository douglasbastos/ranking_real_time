#coding: utf-8

import random

from django.core.management.base import BaseCommand, CommandError
from ranking_real_time.models import Player

import redis
cache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


class Command(BaseCommand):
    help = 'Popular tabela de usuários'

    def handle(self, *args, **options):
        novos_players = self.inserir_usuarios()
        novos = 0
        ja_existe = 0
        print 'Tentando inserir os {} usuários'.format(len(novos_players))
        for player in novos_players:
            try:
                Player.objects.create(username=player, pontos=1000)
                cache.zadd('ranking:username', 1000, player)
                novos += 1
            except:
                ja_existe += 1
        print '{} novos usuários cadastrados com sucesso'.format(novos)
        print '{} não foi possivel inserir, poís já existem no banco de dados'.format(ja_existe)

    def inserir_usuarios(self):
        