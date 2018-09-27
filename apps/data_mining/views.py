from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import status

from utils.permissions import IsOwnerOrReadOnly
from users.models import UserProfile
from tasks.models import TaskInfo, DataSet
from .models import Regression
from .serializers import RegressionSerializer, RegressionDetailSerializer
from db_tools import dataProcessing, dataAnalyze, dataMining
from db_tools import transformer


import os
import logging
import time


# Create your views here.

#  <数据挖掘方法>


class RegressionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示用户所有的回归分析模型
    update:
        更新模型信息
    partial_update:
        更新部分模型信息
    create:
        创建回归分析模型
    delete:
        删除回归分析
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = RegressionSerializer

    def create(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data_set = DataSet.objects.get(id=serializer.data['data_set'])
        taskinfo = TaskInfo.objects.get(id=data_set.task)

        model = Regression.objects.get(id=serializer.data["id"])
        data = dataMining.Process(data_set.step3, taskinfo.task_folder).regression(serializer.data['category'], serializer.data['x_axis'],
                                                                                   serializer.data['y_axis'], serializer.data['xlabel'],
                                                                                   serializer.data['ylabel'],serializer.data['test_size'],
                                                                                   serializer.data['mth_power'], serializer.data['error_type'])

        # 生成图表保存文件
        return Response({"message": "本回归模型创建成功", "data": serializer.data, "code": "201"}, status=status.HTTP_201_CREATED,
                        headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return RegressionSerializer
        elif self.action == "retrieve":
            return RegressionSerializer
        elif self.action == "update":
            return RegressionSerializer

        return RegressionDetailSerializer

    def get_queryset(self):
        return Regression.objects.filter(user=self.request.user)
