# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 30

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getServerDir', views.GetServerDir),
    url(r'^image2base64$', views.image2base64)

]
