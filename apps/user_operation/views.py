import paramiko
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status

from utils.permissions import IsOwnerOrReadOnly
from .models import UserTask, Publish
from tasks.models import TaskInfo, DataSet, Chart
from .serializers import UserTaskSerializer, PublishSerializer


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
        return Publish.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        path = "/home/ZoomInDataSet/"  # 服务器路径
        source_task = TaskInfo.objects.get(id=serializer.data["source_task"])
        task = TaskInfo.objects.create(user=serializer.data["user"], task_name=serializer.data["task_name"],
                                       data_num=source_task.data_num, task_desc=source_task.task_desc,)
        task.task_folder = path + str(task.id)
        task.save()
        # 遍历source_task 对应的dataset、chart、data_mining各个实体，复制其路径下文件，同时创建记录
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == "list":
            return UserTaskSerializer
        elif self.action == "create":
            return PublishSerializer

        return UserTaskSerializer

@api_view(['POST'])
def GetServerDir(request):
    # host_name = '127.0.0.1'
    # user_name = 'root'
    # password = 'BNU123>0808'
    # port = 22
    #
    # #连接远程服务器
    # t = paramiko.Transport((host_name, port))
    # t.connect(username=user_name, password=password)
    # sftp = paramiko.SFTPClient.from_transport(t)
    # data_set = DataSet.objects.filter(task=request.data['task_id'])
    # #进行判断是否为null
    # savePath = request.data['save_path']  # 本地存放的路径
    # if len(data_set) > 0:
    #     Record_dir = ""
    #     #下载
    #     for i in range(len(data_set)):
    #         local_dir = savePath + "/" + data_set[i].step3.split('/')[-1]      #完整本地路径
    #         server_dir = data_set[i].step3
    #         sftp.get(server_dir , local_dir)
    #         Record_dir = local_dir + " "
    #     sftp.close()
    #     return Response({"message": "下载的文件本地路径成功", "data": Record_dir})
    # else:
    return Response({"message": "服务器没有该文件"})



