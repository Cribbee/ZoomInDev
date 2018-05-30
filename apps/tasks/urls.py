# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 30

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/getJsonFile$', views.jsonUpload),
    url(r'^/dataProcessing$', views.DataProcessing),


]
