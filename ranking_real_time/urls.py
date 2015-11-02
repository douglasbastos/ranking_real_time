# coding: utf-8
from django.conf.urls import url

from .views import mysql, redis

urlpatterns = [
    url(r'mysql/votacao/(?P<qnt>[0-9]+)/', mysql, name='ranking_com_mysql'),
    url(r'redis/votacao(?P<qnt>[0-9]+)/', redis, name='ranking_com_redis'),
]
