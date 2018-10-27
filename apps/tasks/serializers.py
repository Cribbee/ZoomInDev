# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 12

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import TaskInfo, DataSet, Chart


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TaskInfo
        validators = [
            UniqueTogetherValidator(
                queryset=TaskInfo.objects.all(),
                fields=('user', 'task_name'),
                message="该任务名已存在"
            )
        ]

        fields = ("user", "id", "task_name", "task_desc")


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskInfo
        fields = ("id", "user", "task_name", "task_desc", "status_type", "add_time", "data_num")


class DataSetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = DataSet
        fields = ("user", "id", "task", "title", "step1", "step2", "step3", "stepX1")


class DataSetDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ("id", "task", "user", "title", "desc", "add_time")


class DataSetProcessingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = DataSet
        fields = ("user",)


class ChartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Chart
        validators = [
            UniqueTogetherValidator(
                queryset=Chart.objects.all(),
                fields=('user', 'title'),
                message="该图表标题已存在"
            )
        ]
        fields = ("id", "user", "data_set", "title","sort","sort_value", "desc", "filter","chart_type","chart_method",
                  "x_axis", "y_axis", "contrast_axis", "secondary_axis","chart_type_2nd","chart_method_2nd")


class ChartDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Chart

        fields = ("id", "user", "data_set", "title", "sort","sort_value","desc","filter", "chart_type","chart_method","x_axis", "y_axis",
                  "contrast_axis", "secondary_axis","chart_type_2nd", "chart_method_2nd","add_time", "updated_time", "chart_folder",)


