import shutil

from collections import OrderedDict
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
from .models import TaskInfo, DataSet, Chart
from .serializers import TaskSerializer, TaskDetailSerializer, DataSetSerializer, DataSetDetailSerializer, \
    DataSetProcessingSerializer, ChartSerializer, ChartDetailSerializer

import codecs
import json
import os
import logging
import time
import pandas as pd

from db_tools import dataProcessing, dataAnalyze
from db_tools import transformer


@api_view(['GET', 'POST'])
def jsonUpload(request):
    if request.method == 'POST':
        return Response({"message": "Json文件保存成功!data中展示接收的数据", "data": request.data})
    return Response({"message": "Please Use POST-method"})


@api_view(['GET', 'POST'])
def DataProcessing(request):
    if request.method == 'POST':
        # path = "D:\\Task\\8211.json"
        path = "/home/ZoomInDev/csv2json.json"
        # fw = codecs.open("/Users/sharb/Downloads/csv2json.json", 'r', 'utf-8')
        fw = codecs.open(path, 'r', 'utf-8')
        ls = json.load(fw)
        return Response({"message": "数据预处理已完成，data中为处理过后的数据表", "data": request.data})

    return Response({"message": "Please Use POST-method"})


@api_view(['GET'])
def scoreAnalysis(request):
    # path = "D:\\Task\\8211.json"
    fw = codecs.open("/home/ZoomInDev/csv2json2222.json", 'r', 'utf-8')
    # fw = codecs.open(path, 'r', 'utf-8')
    ls = json.load(fw)
    return Response({"message": "展示成绩单JSON数据", "data": ls})


# 查看上传后的文件
@api_view(['POST'])
def show_data_set1(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    path = "/home/ZoomInDataSet/test1.json"  # 服务器路径
    # path = "/Users/sharb/Downloads/test1.json"  # 本机的路径
    # path = "D:\\Test\\test1.json"  # windos 路径
    transformer.trans(json_path=path, csv_path=data_set.step3).csv2json()
    ds = codecs.open(path, 'r', 'utf-8')
    ls = json.load(ds)
    os.remove(path)
    return Response({"message": "展示数据处理中的数据集文件", "data": ls})


# 查看上传后的文件
@api_view(['POST'])
def show_data_set3(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    df = pd.read_csv(data_set.step3)
    path = "/home/ZoomInDataSet/test1.json"  # 服务器路径
    # path = "/Users/cribbee/Downloads/test1.json"  # 本机的路径
    # path = "D:\\Test\\test2.json"  # windos 路径
    # transformer.trans(json_path=path, csv_path=data_set.step3).csv2json()
    # ds = codecs.open(path, 'r', 'utf-8')
    # ls = json.load(ds, object_pairs_hook=OrderedDict)
    # # os.remove(path)
    js = df.to_json(orient="records", force_ascii=False)
    data = json.loads(js)
    return Response({"message": "展示数据处理中的数据集文件", "data": data})


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
        taskinfo = TaskInfo.objects.get(id=serializer.data["id"])
        logger.debug("user_id is " + str(taskinfo.user))
        path = "/home/ZoomInDataSet/"  # 服务器路径
        # path = "/Users/sharb/Downloads/" # 本地路径
        # path = "D:\\Task\\"  # windos 路径
        taskinfo.task_folder = path + str(serializer.data["id"])
        dataProcessing.process.mkdir(floder=taskinfo.task_folder)
        user = UserProfile.objects.get(id=taskinfo.user_id)
        user.task_num += 1
        taskinfo.save()
        user.save()

        return Response({"message": "任务创建成功", "data": serializer.data, "code": "201"}, status=status.HTTP_201_CREATED,
                        headers=headers)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if os.path.exists(instance.task_folder):
            shutil.rmtree(instance.task_folder)
        self.perform_destroy(instance)
        user = UserProfile.objects.get(id=instance.user_id)
        user.task_num -= 1
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        req_data.__setitem__('title', request.data['title'])
        req_data.__setitem__('step1', request.data['step1'])
        req_data.__setitem__('step2', request.data['step2'])
        req_data.__setitem__('step3', request.data['step3'])
        req_data.__setitem__('stepX1', request.data['stepX1'])
        taskinfo = TaskInfo.objects.get(id=req_data['task'])

        #  每增加一个数据集，TaskInfo.data_num +1
        taskinfo.data_num += 1
        taskinfo.save()
        #  step1、2分别是存储的json文件名与最初始的csv文件名,并存储step3以备数据预处理使用,stepX1文件是数据集的总结性文件
        req_data['step1'] = (str(taskinfo.task_folder) + "/Data/" + str(req_data['task']) + str(taskinfo.user_id) + str(
            taskinfo.data_num) + "1.json")
        req_data['step2'] = (str(taskinfo.task_folder) + "/Data/" + str(req_data['task']) + str(taskinfo.user_id) + str(
            taskinfo.data_num) + "2.csv")
        req_data['step3'] = (str(taskinfo.task_folder) + "/Data/" + str(req_data['task']) + str(taskinfo.user_id) + str(
            taskinfo.data_num) + "3.csv")
        req_data['stepX1'] = (
                str(taskinfo.task_folder) + "/Data/" + str(req_data['task']) + str(taskinfo.user_id) + str(
            taskinfo.data_num) + "sum_up.csv")
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
        #  对保存后的文件做总结表创建操作
        dataProcessing.process(open_path=req_data['step2']).stepX1_save(req_data['step3'], req_data['stepX1'])
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        os.remove(instance.step1)
        os.remove(instance.step2)
        os.remove(instance.step3)
        os.remove(instance.stepX1)
        task = TaskInfo.objects.get(id=instance.task_id)
        task.data_num -= 1
        task.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChartViewset(viewsets.ModelViewSet):
    """
    list:
        展示用户数据集的图表信息
    update:
        更新图表信息
    retrieve:
        展示部分图表信息
    partial_update:
        更新部分图表信息
    create:
        创建图表信息
    delete:
        删除图表
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ChartSerializer

    def create(self, request, *args, **kwargs):
        logger = logging.getLogger('django')
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        chart = Chart.objects.get(id=serializer.data["id"])
        # 生成图表保存文件

        return Response({"message": "图表信息创建成功", "data": serializer.data, "code": "201"}, status=status.HTTP_201_CREATED,
                        headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return ChartSerializer
        elif self.action == "retrieve":
            return ChartSerializer
        elif self.action == "update":
            return ChartSerializer

        return ChartDetailSerializer

    def get_queryset(self):
        return Chart.objects.filter(user=self.request.user)


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


# 字段排序
@api_view(['POST'])
def sorting(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).sorting(request.data['col_name'], request.data['ascending'])
    data_set.save()
    path = "/home/ZoomInDataSet/test1.json"  # 服务器路径
    # path = "/Users/cribbee/Downloads/test1.json"  # 本机的路径
    # path = "D:\\Test\\test1.json"  # windos 路径
    transformer.trans(json_path=path, csv_path=data_set.step3).csv2json()
    ds = codecs.open(path, 'r', 'utf-8')
    ls = json.load(ds)
    os.remove(path)
    return Response({"message": "字段排序已完成", "data": ls, "code": "200"}, status=status.HTTP_200_OK)


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
        dataProcessing.process(open_path=data_set.step3).drop(request.data['drop_fields'], data_set.stepX1)
        data_set.step3 = data_set.step3.replace(".csv", "d.csv")
        data_set.save()
        return Response({"message": "已成功批量删除字段"}, status=status.HTTP_200_OK)


# 批量修改字段名
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly))
@authentication_classes((JSONWebTokenAuthentication, SessionAuthentication))
def reset_columns(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).reset_columns(request.data['reset'], data_set.stepX1)

    # data_set.step3 = data_set.step3.replace(".csv", "r.csv")
    data_set.save()
    return Response({"message": "批量修改字段名已经完成"})


# 展示数据集字段名与字段类型
@api_view(['POST'])
def show_dtypes(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dtypes = dataProcessing.process(open_path=data_set.stepX1).show_dtypes()
    return Response({"message": "展示每列数据类型dtypes", "data": str(dict(dtypes)), "code": "200"}, status=status.HTTP_200_OK)


# 展示字段描述
@api_view(['POST'])
def show_desc(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    desc = dataProcessing.process(open_path=data_set.stepX1).show_desc()
    return Response({"message": "展示每列数据类型描述", "data": str(dict(desc)), "code": "200"}, status=status.HTTP_200_OK)


# 展示源文件列名
@api_view(['POST'])
def show_OriginColumnsName(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    Columns_name = dataProcessing.process(open_path=data_set.stepX1).show_OriginColumnsName()
    return Response({"message": "展示源文件列名", "data": str(dict(Columns_name)), "code": "200"}, status=status.HTTP_200_OK)


# 计算每列的平均值
@api_view(['POST'])
def average(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    average1 = dataProcessing.process(open_path=data_set.step3).average(request.data['key'], data_set.stepX1)
    data_set.save()
    return Response({"message": "求平均值完成", "data": str(average1)})


# 计算列标准差
@api_view(['POST'])
def standardDeviation(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    std1 = dataProcessing.process(open_path=data_set.step3).std(request.data['key'], data_set.stepX1)
    data_set.save()
    return Response({"message": "求标准差完成", "data": str(std1)})


# 计算列方差
@api_view(['POST'])
def variance(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    var1 = dataProcessing.process(open_path=data_set.step3).var(request.data['key'], data_set.stepX1)
    data_set.save()
    return Response({"message": "求方差完成", "data": str(var1)})


# # 求和函数sum，操作两列，并在末尾生成新一列
# @api_view(['POST'])
# def sum(request):
#     data_set = DataSet.objects.get(id=request.data['data_set_id'])
#     dataProcessing.process(open_path=data_set.step3).sum(request.data['col_a'], request.data['col_b'],
#                                                          request.data['col_new'], data_set.stepX1)
#     data_set.save()
#     return Response({"message": request.data['col_a'] + "列与" + request.data['col_b'] + "列求和完成"})
#
#
# # 求差函数sub
# @api_view(['POST'])
# def sub(request):
#     data_set = DataSet.objects.get(id=request.data['data_set_id'])
#     dataProcessing.process(open_path=data_set.step3).sub(request.data['col_a'], request.data['col_b'],
#                                                          request.data['col_new'], data_set.stepX1)
#     data_set.save()
#     return Response({"message": request.data['col_a'] + "列与" + request.data['col_b'] + "列求差完成"})


# 修改字段描述
@api_view(['POST'])
def changeDesc(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.stepX1).changeDesc(request.data['key'])
    data_set.save()
    return Response({"message": "字段描述修改完成"})


# 强制删除违法行并修改类型
@api_view(['POST'])
def force_changeType(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).dropRow(request.data['key'])
    dataProcessing.process(open_path=data_set.step3).changeType(request.data['key'], data_set.stepX1)
    data_set.save()
    return Response({"message": "类型转换完成"})


# 判断有无违法行，若有则回报违规率，若无直接修改
@api_view(['POST'])
def test_changeType(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    result = dataProcessing.process(open_path=data_set.step3).test_changeType(request.data['key'], data_set.stepX1)
    print(result)
    if not result:
        dataProcessing.process(open_path=data_set.step3).changeType(request.data['key'], data_set.stepX1)
        return Response({"message": "类型转换成功"})
    else:
        return Response({"违规率": str(result)})

# 如果数据行包含空值，则删除数据行
@api_view(['POST'])
def dropnan(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    dataProcessing.process(open_path=data_set.step3).dropnan()
    return Response({"message": "去除空值处理完毕"})

# 修改数据标题
@api_view(['POST'])
def changeTitle(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    data_set.title = request.data['new_title']
    data_set.save()
    return Response({"message": "title修改完毕"})


# 修改列名、字段类型、字段描述
@api_view(['POST'])
def resetColumns_name_type_desc(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    result = dataProcessing.process(open_path=data_set.step3).test_changeType(request.data['type_field'],
                                                                              data_set.stepX1)
    if not result:
        dataProcessing.process(open_path=data_set.stepX1).changeDesc(request.data['desc_field'])
        dataProcessing.process(open_path=data_set.step3).changeType(request.data['type_field'], data_set.stepX1)
        dataProcessing.process(open_path=data_set.step3).reset_columns(request.data['reset_field'], data_set.stepX1)
        return Response({"message": "修改成功"})
    else:
        dataProcessing.process(open_path=data_set.step3).reset_columns(request.data['reset_field'], data_set.stepX1)
        return Response({"message": "类型修改失败", "违规率": str(result)})


# 修改列名、字段类型
@api_view(['POST'])
def resetColumns_name_type(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    result = dataProcessing.process(open_path=data_set.step3).test_changeType(request.data['type_field'],
                                                                              data_set.stepX1)
    if not result:
        dataProcessing.process(open_path=data_set.step3).changeType(request.data['type_field'], data_set.stepX1)
        dataProcessing.process(open_path=data_set.step3).reset_columns(request.data['reset_field'], data_set.stepX1)
        return Response({"message": "修改成功"})
    else:
        dataProcessing.process(open_path=data_set.step3).reset_columns(request.data['reset_field'], data_set.stepX1)
        return Response({"message": "类型修改失败", "违规率": str(result)})


# # 生成指定列的rankit
# @api_view(['POST'])
# def TScoreRankit(request):
#     data_set = DataSet.objects.get(id=request.data['data_set_id'])
#     dataProcessing.process(open_path=data_set.step3).TScoreRankit(request.data['Column_name'], data_set.stepX1)
#     return Response({"message": "Rankit列生成完成"})
#
#
# # 生成指定列的rank
# @api_view(['POST'])
# def TscoreRank(request):
#     data_set = DataSet.objects.get(id=request.data['data_set_id'])
#     dataProcessing.process(open_path=data_set.step3).TScoreRank(request.data['Column_name'], data_set.stepX1)
#     return Response({"message": "Rank列生成完成"})
#
#
# # 根据指定列，以及指定层数，生成每个学生对应的层次
# @api_view(['POST'])
# def Score2Layer(request):
#     data_set = DataSet.objects.get(id=request.data['data_set_id'])
#     dataProcessing.process(open_path=data_set.step3).score2Layer(request.data['layers'], request.data['Column_name'], data_set.stepX1)
#     return Response({"message": "layer列生成完成"})
#
#
# # 根据制定列，生成每个学生所在层数的平均值
# @api_view(['POST'])
# def Score2Layer_mean(request):
#     data_set = DataSet.objects.get(id=request.data['data_set_id'])
#     dataProcessing.process(open_path=data_set.step3, stepX_path=data_set.stepX1, newColumnName=request.data['newColumnName']).Layer_average1(
#         request.data['layer_name'], request.data['Column_name'])
#     return Response({"message": "层平均值列生成完成"})


# # newColumnName为新增列名，espression为表达式
# @api_view(['POST'])
# def Expression(request):
#     data_set = DataSet.objects.get(id=request.data['data_set_id'])
#     result = dataProcessing.process(open_path=data_set.step3, stepX_path=data_set.stepX1, newColumnName=request.data['newColumnName']).Expression(request.data['expression'])
#     return Response({"message": str(result)})

@api_view(['POST'])
def zoomin_eval(request):
    data_set = DataSet.objects.get(id=request.data['data_set_id'])
    result = dataProcessing.process(open_path=data_set.step3, stepX_path=data_set.stepX1, newColumnName=request.data['newColumnName']).zoomin_eval(request.data['function'])
    return Response({"message": str(result)})

#  <数据分析方法>

# # 获取图表处理数据
@api_view(['POST'])
def analysis_result(request):
    chart = Chart.objects.get(id=request.data['chart_id'])
    data_set = DataSet.objects.get(id=request.data['data_set'])

    df = dataAnalyze.Process(open_path=data_set.step3).process(
        chart_type=request.data['chart_type'], x_axis=request.data['x_axis'], y_axis=request.data['y_axis'],
        chart_method=request.data['chart_method'], sort = request.data['sort'], sort_value=request.data['sort_value'],
        filter = request.data['filter'],secondary_axis= request.data["secondary_axis"],
        chart_type_2nd=request.data['chart_type_2nd'],chart_method_2nd=request.data['chart_method_2nd'],
        filter_past= request.data['filter_past'],filter_past_logical_type = request.data['filter_past_logical_type'],
    )
    chart.x_axis = request.data['x_axis']
    chart.y_axis = request.data['y_axis']
    chart.filter_past = request.data['filter_past']
    chart.filter_past_logical_type = request.data['filter_past_logical_type']
    chart.sort = request.data['sort']
    chart.sort_value = request.data['sort_value']
    chart.chart_type = request.data['chart_type']
    chart.chart_method = request.data['chart_method']
    chart.filter = request.data['filter']
    chart.chart_method_2nd = request.data['chart_method_2nd']
    chart.chart_type_2nd = request.data['chart_type_2nd']
    chart.updated_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    chart.save()
    return Response({"message": "获取图表处理数据", "data": df.to_json(orient='columns', force_ascii=False, ),
                     "code": "200"}, status=status.HTTP_200_OK)
