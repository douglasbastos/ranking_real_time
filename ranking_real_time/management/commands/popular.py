# coding: utf-8

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ranking_real_time.models import Player

import redis
cache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


class Command(BaseCommand):
    help = 'Popular tabela de usuários'

    def handle(self, *args, **options):
        novos_players = self.insert_user()
        novos = 0
        tentativa = 0
        usernames = map(lambda user: user.username, User.objects.all())
        players_id = map(lambda player: player.pk, Player.objects.all())
        print 'Tentando inserir os {} usuários'.format(len(novos_players))
        for player in novos_players:
            # verifica está cadastrado na base de usuáriso
            if player not in usernames:
                user = User.objects.create(username=player)
            else:
                user = User.objects.get(username=player)

            # verifica se está cadastrado na base de ranking
            if user.pk not in players_id:
                Player.objects.create(username_id=user.pk, pontos=1000)
                cache.zadd('ranking:username', 1000, player)
                novos += 1

            tentativa += 1
            print '{}/{}'.format(tentativa, len(novos_players))
        print '\e[1;32m{} novos usuários cadastrados com sucesso'.format(novos)

    def insert_user(self):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'lista_usuarios.txt')
        items_file = open(file_path, 'r')
        items = items_file.readlines()
        return map(lambda item: item.replace('\n', ''), items)
