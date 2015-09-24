#coding: utf-8

from django.shortcuts import render, get_object_or_404

from .models import Player

import redis
cache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def mysql(request, **kwargs):
    qnt = kwargs['qnt']
    players = Player.objects.all().order_by('-pontos')[:qnt]
    context = {'players': players}
    template = 'ranking_real_time/base.html'
    return render(request, template, context)

def redis(request, **kwargs):
    qnt = int(kwargs['qnt']) - 1
    player = []
    players = []
    players_redis = cache.zrevrange('ranking:username', 0, qnt, True)
    for pl in players_redis:
        players.append({'username': pl[0], 'pontos': int(pl[1])})
    context = {'players': players}
    template = 'ranking_real_time/base.html'
    return render(request, template, context)
