import os
import shutil
from datetime import datetime

import paramiko
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from utils.permissions import IsOwnerOrReadOnly
from .models import UserTask, Publish, Summary
from tasks.models import TaskInfo, DataSet, Chart
from users.models import UserProfile
from data_mining.models import Clustering, Regression
from .serializers import UserTaskSerializer, PublishSerializer, PublishDetailSerializer, SummarySerializer
from db_tools import transformer,dataAnalyze



class UserTaskViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏任务
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    #  根据 tasks_id 去查找信息
    lookup_field = "tasks_id"

    #  重载 get_queryset 方法，使得增加验证request 中的user是否正确
    def get_queryset(self):
        return UserTask.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return UserTaskSerializer
        elif self.action == "create":
            return UserTaskSerializer

        return UserTaskSerializer


class PublishViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = PublishSerializer

    def get_queryset(self):
        return Publish.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        path = "/home/ZoomInDataSet/"  # 服务器路径
        # path = "D:\\Task\\"  # windos 路径
        # 获取源任务对象
        source_task = TaskInfo.objects.get(id=serializer.data["source_task"])
        # 新建分享任务
        task = TaskInfo.objects.create(user_id=serializer.data["shared_user"], task_name=serializer.data["task_name"],
                                       data_num=source_task.data_num, task_desc=source_task.task_desc)

        # 新建任务后完善publish表
        Publish_model = Publish.objects.get(id=serializer.data["id"])
        Publish_model.task = task.id
        Publish_model.save()

        # 根据task.id更新分享任务的文件路径
        task.task_folder = path + str(task.id)
        task.save()

        # 新建文件夹并拷贝文件夹
        os.mkdir('/home/ZoomInDataSet/Publish/' + task.id)
        shutil.copytree(source_task.task_folder, task.task_folder)

        # 遍历source_task 对应的dataset、chart、data_mining各个实体，复制其路径下文件，同时创建记录
        # dataset表
        #
        # 到Publish文件夹
        for i in DataSet.objects.filter(task_id=source_task.id):
            i.id = None
            i.step1 = transformer.trans_taskid(i.step1, str(task.id))
            i.step2 = transformer.trans_taskid(i.step2, str(task.id))
            i.step3 = transformer.trans_taskid(i.step3, str(task.id))
            i.stepX1 = transformer.trans_taskid(i.stepX1, str(task.id))
            i.task_id = task.id
            i.user_id = task.user_id
            i.add_time = datetime.now()
            i.save()

            # chart表
            for c in Chart.objects.filter(data_set=i.id, chart_folder1__isnull=False):
                c.id = None
                c.data_set = i.id
                c.chart_folder = transformer.copy_dataAnalyzeImages(c.chart_folder2)
                c.add_time = datetime.now()
                c.updated_time = None
                c.user_id = task.user_id
                c.save()

            # data_mining_clustering表
            for k in Clustering.objects.filter(data_set=i.id):
                k.id = None
                k.data_set = i.id
                if k.chart_folder1 is not None:
                    k.chart_folder1 = transformer.copy_dataMiningImages(k.chart_folder1, str(task.id))
                if k.chart_folder2 is not None:
                    k.chart_folder2 = transformer.copy_dataMiningImages(k.chart_folder2, str(task.id))
                k.add_time = datetime.now()
                k.updated_time = None
                k.user_id = task.user_id
                k.save()

            # data_mining_regression表
            for s in Regression.objects.filter(data_set=i.id):
                s.id = None
                s.data_set = i.id
                if s.chart_folder1 is not None:
                    s.chart_folder1 = transformer.copy_dataMiningImages(s.chart_folder1, str(task.id))
                if s.chart_folder2 is not None:
                    s.chart_folder2 = transformer.copy_dataMiningImages(s.chart_folder2, str(task.id))
                s.add_time = datetime.now()
                s.updated_time = None
                s.user_id = task.user_id
                s.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == "list":
            return PublishSerializer
        elif self.action == "create":
            return PublishSerializer
        elif self.action == "retrieve":
            return PublishDetailSerializer
        elif self.action == "shared":
            return PublishSerializer

        return PublishSerializer


class SummaryViewset(viewsets.ModelViewSet):
    """
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = SummarySerializer

    def get_queryset(self):
        return Summary.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == "list":
            return SummarySerializer
        elif self.action == "create":
            return SummarySerializer

        return SummarySerializer


@api_view(['POST'])
def image2base64(request):
    result = transformer.images2base64(request.data['image_url'])
    return Response({"message": result})


@api_view(['POST'])
def publish(request):
    result = {}
    user = UserProfile.objects.get(id=request.user.id)
    result['user_name'] = user.username
    task = TaskInfo.objects.get(id=request.data['task_id'])
    result['add_time'] = task.add_time
    data_set = DataSet.objects.filter(task_id=request.data['task_id'])
    list1 = []
    for i in data_set:
        dict1 = {}
        dict1['data_set_name'] = i.title
        chart_num = 1
        clustering_num = 1
        regression_num = 1
        for c in Chart.objects.filter(data_set=i.id, chart_folder1__isnull=False):
            dict1['data_analyze_' + chart_num] = c.chart_folder2
            chart_num = chart_num + 1
        for k in Clustering.objects.filter(data_set=i.id):
            if k.chart_folder1 is not None:
                dict1['data_mining_clustering1_' + str(clustering_num)] = k.chart_folder1
            if k.chart_folder2 is not None:
                dict1['data_mining_clustering2_' + str(clustering_num)] = k.chart_folder2
            if k.chart_folder1 or k.chart_folder2:
                clustering_num = clustering_num + 1
        for s in Regression.objects.filter(data_set=i.id):
            if s.chart_folder1 is not None:
                dict1['data_mining_regression1_' + str(regression_num)] = s.chart_folder1
            if s.chart_folder2 is not None:
                dict1['data_mining_regression2_' + str(regression_num)] = s.chart_folder2
            if s.chart_folder1 or s.chart_folder2:
                regression_num = regression_num + 1
        list1.append(dict1)
    result['data_set'] = list1
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def GetServerDir(request):
    host_name = '127.0.0.1'
    user_name = 'root'
    password = 'BNU123>0808'
    port = 22
    # 应该加上权限认证
    # 连接远程服务器
    t = paramiko.Transport((host_name, port))
    t.connect(username=user_name, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    data_set = DataSet.objects.filter(task=request.data['task_id'])
    # 进行判断是否为null
    savePath = request.data['save_path']  # 本地存放的路径
    if len(data_set) > 0:
        Record_dir = ""
        # 下载
        for i in range(len(data_set)):
            local_dir = savePath + "/" + data_set[i].step3.split('/')[-1]  # 完整本地路径
            server_dir = data_set[i].step3
            sftp.get(server_dir, local_dir)
            Record_dir = local_dir + " "
        sftp.close()
        return Response({"message": "下载的文件本地路径成功", "data": Record_dir})
    else:
        return Response({"message": "服务器没有该文件"})


@api_view(['POST'])
def show_chart(request):
    info = {}
    summary = Summary.objects.get(id=request.data['summary'])

    data_sets = DataSet.objects.filter(task=summary.task.id)

    chart_sort = summary.task_chart
    if len(chart_sort) == 0:
        chart_sort = {}
    for data_set in data_sets:
        charts = Chart.objects.filter(data_set=data_set.id).order_by('-updated_time')
        Clustering_charts = Clustering.objects.filter(data_set=data_set.id).order_by('-updated_time')
        Regression_charts = Regression.objects.filter(data_set=data_set.id).order_by('-updated_time')
        info, chart_sort = dataAnalyze.chart_sort(chart_sort).show_chart(charts, info, chart_sort)
        info, chart_sort = dataAnalyze.chart_sort(chart_sort).show_Clustering_charts(Clustering_charts, info, chart_sort)
        info, chart_sort = dataAnalyze.chart_sort(chart_sort).show_Regression_charts(Regression_charts, info,chart_sort)

        print(chart_sort)
        summary.task_chart = chart_sort
        summary.save()

    return Response(
        {"message": "该任务下的图表信息", "data": chart_sort, "code": "201"},
        status=status.HTTP_200_OK)


@api_view(['POST'])
def change_sort(request):
    summary = Summary.objects.get(id = request.data['summary'])
    summary.task_chart = request.data['task_chart']
    summary.save()
    return Response(
        {"message": "该任务下的图表信息", "data":summary.id, "code": "201"},
        status=status.HTTP_200_OK)


