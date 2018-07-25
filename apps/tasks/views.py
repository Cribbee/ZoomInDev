from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import status

from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend

from utils.permissions import IsOwnerOrReadOnly
from users.models import UserProfile
from .models import TaskInfo, DataSet
from .serializers import TaskSerializer, TaskDetailSerializer, DataSetSerializer, DataSetDetailSerializer,\
                         DataSetProcessingSerializer


import codecs
import json
import os
import logging

from db_tools import dataProcessing
from db_tools import dirProcessing
from db_tools import transformer


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


#查看上传后的文件
@api_view(['POST'])
def show_data_set1(request):

    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    # 服务器路径："/home/ZoomInDataSet/test1.json"
    # 本机的路径："/Users/cribbee/Downloads/test1.json"
    transformer.trans(json_path="/home/ZoomInDataSet/test1.json", csv_path=data_set.step2).csv2json()
    ds = codecs.open("/home/ZoomInDataSet/test1.json", 'r', 'utf-8')
    ls = json.load(ds)
    os.remove("/home/ZoomInDataSet/test1.json")
    return Response({"message": "展示上传后的数据文件", "data": ls})


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

    def create(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        logger.debug("task_id is " + str(serializer.data["id"]))
        taskinfo = TaskInfo.objects.get(id= serializer.data["id"])
        logger.debug("user_id is " + str(taskinfo.user))
        # 服务器路径:"/home/ZoomInDataSet/"
        # 本地路径："/Users/cribbee/Downloads/"
        taskinfo.task_folder = "/home/ZoomInDataSet/" + str(serializer.data["id"])
        dataProcessing.process.mkdir(floder=taskinfo.task_folder)
        user = UserProfile.objects.get(id=taskinfo.user_id)
        user.task_num += 1
        taskinfo.save()
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

    def create(self, request, *args, **kwargs):

        logger = logging.getLogger('django')
        data_set = request.data['data_set']
        row_num = request.data['row_num']
        req_data = {}
        req_data.__setitem__('task', request.data['task'])
        req_data.__setitem__('step1', request.data['step1'])
        req_data.__setitem__('step2', request.data['step2'])
        req_data.__setitem__('step2', request.data['step3'])
        taskinfo = TaskInfo.objects.get(id=req_data['task'])

        #  每增加一个数据集，TaskInfo.data_num +1
        taskinfo.data_num += 1
        taskinfo.save()
        #  step1、2分别是存储的json文件名与最初始的csv文件名,并存储step3以备数据预处理使用
        req_data['step1'] = (str(taskinfo.task_folder)+"/Data/"+str(req_data['task']) + str(taskinfo.user_id) + str(taskinfo.data_num) + "1.json")
        req_data['step2'] = (str(taskinfo.task_folder)+"/Data/"+str(req_data['task']) + str(taskinfo.user_id) + str(taskinfo.data_num) + "2.csv")
        req_data['step3'] = (str(taskinfo.task_folder)+"/Data/"+str(req_data['task']) + str(taskinfo.user_id) + str(taskinfo.data_num) + "3.csv")

        logger.debug("data_set_name is " + str(req_data['step1']))

        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #  初始json文件保存
        dataProcessing.process(open_path=req_data['step1']).original_save(data_set)
        #  对data_set做json2csv转换
        transformer.trans(json_path=req_data['step1'], csv_path=req_data['step2']).json2csv()
        #  对data_set进行csv文件格式下的祛除表头操作
        dataProcessing.process(open_path=req_data['step2']).step2_save(int(row_num))
        #  对保存后的文件复制保存以备数据处理使用
        dataProcessing.process(open_path=req_data['step2']).step3_save(req_data['step3'])
        return Response(data=({"message": "数据上传已完成", "data": serializer.data, "code": "201"}),
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == "list":
            return DataSetDetailSerializer
        elif self.action == "partial_update":
            return DataSetDetailSerializer
        elif self.action == "create":
            return DataSetSerializer
        return DataSetDetailSerializer

    def get_queryset(self):
        return DataSet.objects.filter(user=self.request.user)


#  <数据预处理方法>

#  处理缺失值
@api_view(['POST'])
def missing_value(request):

    data_set = DataSet.objects.get(id=request.data['id'])
    dataProcessing.process(open_path=data_set.step3).missing_value(axis=request.data['axis'], how=request.data['how'])
    data_set.step3 = data_set.step3.replace(".csv", "m.csv")
    data_set.save()
    return Response({"message": "缺失值处理已完成"})


#  条件过滤
@api_view(['POST'])
def filters(request):
    logger = logging.getLogger('django')
    logger.debug("req_data is " + str(request.data['filter']))

    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).filter_processing(request.data['logical_type'],
                                                                       request.data['filter'])

    data_set.step3 = data_set.step3.replace(".csv", "f.csv")
    data_set.save()
    return Response({"message": "过滤处理已完成"})


# 添加序号列
@api_view(['POST'])
def set_index(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).set_index()

    data_set.step3 = data_set.step3.replace(".csv", "i.csv")
    data_set.save()
    return Response({"message": "序号列添加已完成"})


# 求和函数sum，操作两列，并在末尾生成新一列
@api_view(['POST'])
def sum(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).sum(request.data['col_a'], request.data['col_b'], request.data['col_new'])
    data_set.save()
    return Response({"message": request.data['col_a'] + "列与" + request.data['col_b'] + "列求和完成"})


class DelValue(APIView):
    """
    批量删除列
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get(self, request):
        return HttpResponse('message：请使用POST方法')

    def post(self, request):
        serializer = DataSetProcessingSerializer(data=request.data)
        data_set = DataSet.objects.get(id=request.data['data_set_id'])
        dataProcessing.process(open_path=data_set.step3).drop(request.data['drop_fields'])
        data_set.step3 = data_set.step3.replace(".csv", "d.csv")
        data_set.save()
        return Response({"message": "已成功批量删除字段"}, status=status.HTTP_200_OK)


# 批量修改字段名
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
def reset_columns(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).reset_columns(request.data['reset'])

    data_set.step3 = data_set.step3.replace(".csv", "r.csv")
    data_set.save()
    return Response({"message": "批量修改字段名已经完成"})









