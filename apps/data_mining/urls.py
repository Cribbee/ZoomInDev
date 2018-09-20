# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 30

from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^dataProcessing/missingValue$', views.missing_value),
    url(r'^dataProcessing/filters$', views.filters),
    url(r'^dataProcessing/setIndex$', views.set_index),




]
