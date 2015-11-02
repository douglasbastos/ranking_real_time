# coding: utf-8
from django.conf.urls import url

from .views import mysql, redis

urlpatterns = [
    url(r'mysql/(?P<qnt>[0-9]+)/', mysql, name='ranking_com_mysql'),
    url(r'redis/(?P<qnt>[0-9]+)/', redis, name='ranking_com_redis'),
]
