# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 12

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import TaskInfo, DataSet


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

    class Meta:
        model = DataSet
        fields = ("task", "step1")


class DataSetDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = ("id", "task", "title", "desc", "chart_type", "x_axis", "y_axis", "add_time")