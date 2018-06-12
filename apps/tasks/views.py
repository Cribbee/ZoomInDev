from rest_framework import viewsets
from rest_framework import mixins
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
from .serializers import TaskSerializer, TaskDetailSerializer
from db_tools import json2csv

import codecs
import json
import os


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





