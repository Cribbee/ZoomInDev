# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 9 / 20

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Regression


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

