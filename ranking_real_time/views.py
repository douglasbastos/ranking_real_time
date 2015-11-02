# coding: utf-8

from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import never_cache
from .models import Player

import redis
cache = redis.StrictRedis(host=settings.REDIS_DB['host'],
                          port=settings.REDIS_DB['port'],
                          db=settings.REDIS_DB['db'])


@never_cache
def mysql(request, **kwargs):
    qnt = kwargs['qnt']
    players = Player.objects.all().order_by('-pontos')[:qnt]
    context = {'players': players}
    template = 'ranking_real_time/base.html'
    return render(request, template, context)


@never_cache
def redis(request, **kwargs):
    qnt = int(kwargs['qnt']) - 1
    players = []
    players_redis = cache.zrevrange('ranking:username', 0, qnt, True)
    for pl in players_redis:
        players.append({'username': pl[0], 'pontos': int(pl[1])})
    context = {'players': players}
    template = 'ranking_real_time/base.html'
    return render(request, template, context)
