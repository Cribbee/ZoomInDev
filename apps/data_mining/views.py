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
from .models import Regression, Clustering
from .serializers import RegressionSerializer, RegressionDetailSerializer, ClusteringDetailSerializer, ClusteringSerializer
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
        taskinfo = TaskInfo.objects.get(id=data_set.task_id)

        upload_folder = "/home/ZoomInDataSet/DataMining/Regression/"
        model = Regression.objects.get(id=serializer.data["id"])
        data = dataMining.Process(data_set.step3, taskinfo.task_folder, upload_folder).regression(serializer.data['title'], serializer.data['category'], serializer.data['x_axis'],
                                                                                   serializer.data['y_axis'], serializer.data['xlabel'],
                                                                                   serializer.data['ylabel'],serializer.data['test_size'],
                                                                                   serializer.data['mth_power'], request.data['error_type'])
        if serializer.data['category'] == 11:
            model.chart_folder1 = data[1]
            model.save()
            return Response({"message": "本回归模型创建成功", "data": ["chart_folder1: "+data[1], "error_sum: "+str(data[0])], "code": "201"},
                            status=status.HTTP_201_CREATED, headers=headers)
        if serializer.data['category'] == 12:
            model.chart_folder1 = data[0]
            model.chart_folder2 = data[1]
            model.save()
            return Response({"message": "本回归模型创建成功", "data": ["chart_folder1: "+data[0], "chart_folder2: "+data[1]], "code": "201"},
                            status=status.HTTP_201_CREATED, headers=headers)

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


#聚类模型
class ClusteringViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    用户认证
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ClusteringSerializer

    #传递参数
    def create(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data_set = DataSet.objects.get(id=serializer.data['data_set'])      #数据集AD      接收传过来的参数
        taskinfo = TaskInfo.objects.get(id=data_set.task_id)                #任务ID

        upload_folder = "/home/ZoomInDataSet/DataMining/Clustering/"

        model = Clustering.objects.get(id=serializer.data["id"])            #3
        #strp3路径，D/task路径             传过去文件路径，文件夹的起始路径
        data = dataMining.Process(data_set.step3, taskinfo.task_folder,
                                  upload_folder).clustering(serializer.data['title'], serializer.data['category'],
                                                                                      serializer.data['k_clustering'],
                                                                                      serializer.data['Datacsv_list'],
                                                                                      serializer.data['random_state'],
                                                                                      serializer.data['max_iter'],
                                                                                      serializer.data['batch_size'],
                                                                                      serializer.data['n_init'],
                                                                                      serializer.data['reassignment_ratio'],)
        #聚类
        if serializer.data['category'] == 13:
            if len(serializer.data['Datacsv_list'].split(',')) == 1:
                model.chart_folder0 = data[0]
                model.chart_folder1 = data[1]
                model.chart_folder2 = data[2]
                model.chart_folder3 = data[3]
                model.save()
                return Response({"message": "Kmeans聚类一维模型创建成功", "data": ["chart_folder1: " + data[0], "chart_folder2: " + data[1], "chart_folder3: " + data[2], "chart_folder4: " + data[3]],
                                 "code": "201"},
                                status=status.HTTP_201_CREATED, headers=headers)
            else:
                model.chart_folder0 = data[0]
                model.chart_folder1 = data[1]
                model.save()
                return Response({"message": "Kmeans聚类二维模型创建成功",
                                 "data": ["chart_folder1: " + data[0], "chart_folder2: " + data[1], ],
                                 "code": "201"},
                                status=status.HTTP_201_CREATED, headers=headers)
        if serializer.data['category'] == 14:
            if len(serializer.data['Datacsv_list'].split(',')) == 1:
                model.chart_folder0 = data[0]
                model.chart_folder1 = data[1]
                model.chart_folder2 = data[2]
                model.chart_folder3 = data[3]
                model.save()
                return Response({"message": "MiniBatch聚类一维模型创建成功", "data": ["chart_folder1: " + data[0], "chart_folder2: " + data[1], "chart_folder3: " + data[2], "chart_folder4: " + data[3]],
                                 "code": "201"},
                                status=status.HTTP_201_CREATED, headers=headers)
            else:
                model.chart_folder0 = data[0]
                model.chart_folder1 = data[1]
                model.save()
                return Response({"message": "MiniBatch聚类二维模型创建成功",
                                 "data": ["chart_folder1: " + data[0], "chart_folder2: " + data[1], ],
                                 "code": "201"},
                                status=status.HTTP_201_CREATED, headers=headers)

        # 生成图表保存文件
        return Response({"message": "本聚类模型创建成功", "data": serializer.data, "code": "201"},
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return ClusteringSerializer
        elif self.action == "retrieve":
            return ClusteringSerializer
        elif self.action == "update":
            return ClusteringSerializer

        return ClusteringDetailSerializer

    def get_queryset(self):
        return Clustering.objects.filter(user=self.request.user)


