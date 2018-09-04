# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 30

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/getJsonFile$', views.jsonUpload),
    url(r'^/dataProcessing$', views.DataProcessing),
    url(r'^/scoreAnalysis$', views.scoreAnalysis),
    url(r'^/dataProcessing/missingValue$', views.missing_value),
    url(r'^/dataProcessing/filters$', views.filters),
    url(r'^/dataProcessing/setIndex$', views.set_index),
    url(r'^/dataProcessing/sum$', views.sum),
    url(r'^/dataProcessing/showDataSet1$', views.show_data_set1),
    url(r'^/dataProcessing/showDataSet3$', views.show_data_set3),
    url(r'^/dataProcessing/resetColumn$', views.reset_columns),
    url(r'^/dataProcessing/showDtypes$', views.show_dtypes),
    url(r'^/dataProcessing/sorting$', views.sorting),
    url(r'^/dataProcessing/average$', views.average),
    # url(r'^/dataProcessing/standardDeviation/', views.standardDeviation),
    # url(r'^/dataProcessing/variance/', views.variance),
    # url(r'^/dataProcessing/sub/', views.sub)



]
