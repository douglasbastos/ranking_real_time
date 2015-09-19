#coding: utf-8

import random

from django.core.management.base import BaseCommand, CommandError
from ranking_real_time.models import Player

import redis
cache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

class Command(BaseCommand):
    help = 'Popular tabela de usuários'

    def handle(self, *args, **options):
        pass