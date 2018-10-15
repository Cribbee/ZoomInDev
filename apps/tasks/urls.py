# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 30

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getJsonFile$', views.jsonUpload),
    url(r'^dataProcessing$', views.DataProcessing),
    url(r'^scoreAnalysis$', views.scoreAnalysis),
    url(r'^dataProcessing/missingValue$', views.missing_value),
    url(r'^dataProcessing/filters$', views.filters),
    url(r'^dataProcessing/setIndex$', views.set_index),
    url(r'^dataProcessing/sum$', views.sum),
    url(r'^dataProcessing/showDataSet1$', views.show_data_set1),
    url(r'^dataProcessing/showDataSet3$', views.show_data_set3),
    url(r'^dataProcessing/resetColumn$', views.reset_columns),
    url(r'^dataProcessing/showDtypes$', views.show_dtypes),
    url(r'^dataProcessing/sorting$', views.sorting),
    url(r'^dataProcessing/average$', views.average),
    url(r'^dataProcessing/standardDeviation$', views.standardDeviation),
    url(r'^dataProcessing/variance$', views.variance),
    url(r'^dataProcessing/sub$', views.sub),
    url(r'^dataProcessing/changeType$', views.force_changeType),
    url(r'^dataProcessing/changeDesc$', views.changeDesc),
    url(r'^chart/sum$', views.sum_analysis),
    url(r'^chart/mean$', views.mean_analysis),
    url(r'^dataProcessing/test_changeType$', views.test_changeType),
    url(r'^dataProcessing/resetColumns_name_type_desc$', views.resetColumns_name_type_desc),
    url(r'^dataProcessing/resetColumns_name_type$', views.resetColumns_name_type),
    url(r'^dataProcessing/showDesc$', views.show_desc),
    url(r'^dataProcessing/showOriginColumnsName$', views.show_OriginColumnsName),
    url(r'^dataProcessing/TscoreRank', views.TscoreRank),
    url(r'^dataProcessing/TscoreRankit', views.TScoreRankit),
    url(r'^dataProcessing/Score2Layer', views.Score2Layer),
    url(r'^dataProcessing/Score2Layer_mean', views.Score2Layer_mean)

]
