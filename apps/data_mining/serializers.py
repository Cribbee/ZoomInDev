# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 9 / 20

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Regression,Modelclustering


class RegressionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Regression
        validators = [
            UniqueTogetherValidator(
                queryset=Regression.objects.all(),
                fields=('user', 'title'),
                message="该模型的图表标题已存在"
            )
        ]
        fields = ("id", "user", "data_set", "title", "desc", "category", "xlabel", "ylabel", "x_axis",
                  "y_axis", "test_size", "mth_power", "error_type", "chart_folder1", "chart_folder2")


class RegressionDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Regression

        fields = ("id", "user", "data_set", "title", "desc", "category", "x_axis", "y_axis",
                  "test_size", "mth_power", "error_type", "add_time", "updated_time", "chart_folder1", "chart_folder2")

class ClusteringSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Modelclustering
        validators = [
            UniqueTogetherValidator(
                queryset=Modelclustering.objects.all(),
                fields=('user', 'title'),
                message="该模型的图表标题已存在"
            )
        ]
        fields = ("id", "user", "data_set", "title", "desc", "category"
                  , "k_clustering","Datacsv_list","random_state", "max_iter","batch_size","n_init","reassignment_ratio", "chart_folder1", "chart_folder2")


class ClusteringDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Modelclustering
        fields = ("id", "user", "data_set", "title", "desc", "category"
                  , "k_clustering", "Datacsv_list", "random_state","max_iter","batch_size","n_init","reassignment_ratio","add_time","updated_time", "chart_folder1", "chart_folder2")


