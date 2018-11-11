import shutil
from datetime import datetime

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
from .models import UserTask, Publish
from . import tests
from tasks.models import TaskInfo, DataSet, Chart
from users.models import UserProfile
from data_mining.models import Clustering, Regression
from .serializers import UserTaskSerializer, PublishSerializer, PublishDetailSerializer, SummarySerializer


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

        # path = "/home/ZoomInDataSet/"  # 服务器路径
        path = "D:\\Task\\"  # windos 路径
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
        shutil.copytree(source_task.task_folder, task.task_folder)

        # 遍历source_task 对应的dataset、chart、data_mining各个实体，复制其路径下文件，同时创建记录
        # dataset表
        for i in DataSet.objects.filter(task_id=source_task.id):
            i.id = None
            i.step1 = tests.trans(i.step1, str(task.id))
            i.step2 = tests.trans(i.step2, str(task.id))
            i.step3 = tests.trans(i.step3, str(task.id))
            i.stepX1 = tests.trans(i.stepX1, str(task.id))
            i.task_id = task.id
            i.user_id = task.user_id
            i.add_time = datetime.now()
            i.save()

            # data_mining_clustering表
            for k in Clustering.objects.filter(data_set=i.id):
                k.id = None
                k.data_set = i.id
                k.chart_folder1 = tests.trans(k.chart_folder1, str(task.id))
                k.chart_folder2 = tests.trans(k.chart_folder2, str(task.id))
                k.add_time = datetime.now()
                k.updated_time = None
                k.user_id = task.user_id
                k.save()

            # data_mining_regression表
            for s in Regression.objects.filter(data_set=i.id):
                s.id = None
                s.data_set = i.id
                s.chart_folder1 = tests.trans(s.chart_folder1, str(task.id))
                s.chart_folder2 = tests.trans(s.chart_folder2, str(task.id))
                s.add_time = datetime.now()
                s.updated_time = None
                s.user_id = task.user_id
                s.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['POST'])
    def publish(self, request, pk=None):
        result = {}
        user = UserProfile.objects.get(id=request.user)
        result['user_name'] = user.username
        task = TaskInfo.objects.get(id=request.data['task_id'])
        result['add_time'] = task.add_time
        data_set = DataSet.objects.filter(task_id=request.data['task_id'])
        for i in data_set:
            result['data_set_name'] = i.title
            for k in Clustering.objects.filter(data_set=i.id):
                result['data_mining_clustering1'] = k.chart_folder1
                result['data_mining_clustering2'] = k.chart_folder2
            for s in Regression.objects.filter(data_set=i.id):
                result['data_mining_regression1'] = s.chart_folder1
                result['data_mining_regression2'] = s.chart_folder2

        # 再加上 结论表

        return Response(result, status=status.HTTP_200_OK)

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
            return UserTaskSerializer
        elif self.action == "create":
            return SummarySerializer

        return SummarySerializer
