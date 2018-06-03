from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from django_filters.rest_framework import DjangoFilterBackend
from .models import TaskInfo,DataSet
from db_tools import json2csv

import codecs
import json


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





