from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions import IsOwnerOrReadOnly
from .models import TaskInfo,DataSet
from .serializers import TaskSerializer, TaskDetailSerializer, DataSetSerializer
from db_tools.dataProcessing import process

import codecs
import json
import os
import logging

from db_tools import dataProcessing


@api_view(['GET', 'POST'])
def jsonUpload(request):
    if request.method == 'POST':

        return Response({"message": "Json文件保存成功!data中展示接收的数据", "data": request.data})
    return Response({"message": "Please Use POST-method"})


@api_view(['GET', 'POST'])
def DataProcessing(request):
    if request.method == 'POST':
        fw = codecs.open("/Users/cribbee/Downloads/csv2json.json", 'r', 'utf-8')
        ls = json.load(fw)
        return Response({"message": "数据预处理已完成，data中为处理过后的数据表", "data": request.data})

    return Response({"message": "Please Use POST-method"})


@api_view(['GET'])
def scoreAnalysis(request):
    fw = codecs.open("/home/ZoomInDev/csv2json2222.json", 'r', 'utf-8')
    ls = json.load(fw)
    return Response({"message": "展示成绩单JSON数据", "data": ls})


class TaskViewset(viewsets.ModelViewSet):
    """
    list:
        展示用户任务信息
    update:
        更新修改任务信息
    create:
        创建任务
    delete:
        删除任务信息
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TaskDetailSerializer
        elif self.action == "retrieve":
            return TaskDetailSerializer
        elif self.action == "create":
            return TaskSerializer

        return TaskSerializer

    def get_queryset(self):
        return TaskInfo.objects.filter(user=self.request.user)


class DataSetViewset(viewsets.ModelViewSet):
    """
    create:
        上传数据文件
    list:
        查看数据集信息
    update:
        更改数据集标题和描述
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = DataSetSerializer

    def create(self, request, *args, **kwargs):

        logger = logging.getLogger('django')
        logger.debug("data_set is " + request.data['data_set'])
        data_set = request.data['data_set']
        row_num = request.data['row_num']
        req_data = {}
        req_data.__setitem__('task', request.data['task'])
        req_data.__setitem__('step1', request.data['step1'])
        taskinfo = TaskInfo.objects.get(id=req_data['task'])

        #  每增加一个数据集，TaskInfo.data_num +1
        taskinfo.data_num += 1
        taskinfo.save()
        #  step1是存储的文件名
        req_data['step1'] = (req_data['task'] + taskinfo.user + taskinfo.data_num + "1.json")
        logger.debug("data_set is " + req_data['step1'])

        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #  对data_set做json2csv转换


        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # def upload(self):
    #     row_num = self.request.row_num
    #     self.request.data_set = dataProcessing.process("path").orginal_save(row_num)

    def get_queryset(self):
        return DataSet.objects.filter(user=self.request.user)











