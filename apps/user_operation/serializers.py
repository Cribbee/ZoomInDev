# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 5

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserTask, Publish


class UserTaskSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户 使用serializers.HiddenField
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # validate实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserTask.objects.all(),
                fields=('user', 'tasks'),
                #  message的信息可以自定义
                message="已经创建过该项目"
            )
        ]
        model = UserTask
        # 收藏的时候需要返回任务的id，因为取消收藏的时候必须知道任务的id是多少
        fields = ("user", 'id')


# 发布序列化
class PublishSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户 使用serializers.HiddenField
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Publish
        # # validate实现唯一联合，一个商品只能收藏一次
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=UserTask.objects.all(),
        #         fields=('user', 'task_name'),
        #         #  message的信息可以自定义
        #         message="所分享任务名重复"
        #     )
        # ]

        fields = ("user", "id", "shared_user", "source_task", "task_name")


class PublishDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = ("user", "id", "shared_user", "source_task", "task_name")
