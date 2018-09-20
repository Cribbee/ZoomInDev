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
from .models import Regression

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
    # queryset = Regression.objects.all()
    # serializer_class = GoodsSerializer
    # pagination_class = GoodsPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_class = GoodsFilter
    # search_fields = ('name', 'goods_brief', 'goods_desc')
    # ordering_fields = ('sold_num', 'shop_price')
    #
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.click_num += 1
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)