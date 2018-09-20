from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat", on_delete=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "模型类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Regression(models.Model):
    """
    回归分析模型
    """
    ERROR_TYPE = (
        (1, "MSE:均方误差"),
        (2, "MAE:平均绝对误差"),
        (3, "RMSE:均方根误差"),
    )

    user = models.ForeignKey(User, models.CASCADE, null=True, verbose_name="用户ID")
    category = models.ForeignKey(ModelCategory, models.CASCADE, null=True, verbose_name="模型类目")
    data_set = models.IntegerField(verbose_name="数据集ID", default=-1)
    title = models.CharField(max_length=20, verbose_name="标题", default="", help_text="标题")
    desc = models.CharField(max_length=20, verbose_name="描述", blank=True, null=True, default="", help_text="描述")
    x_axis = models.CharField(max_length=200, verbose_name="自变量", blank=True, null=True, default="", help_text="特征项个数区分一元或多元")
    y_axis = models.CharField(max_length=200, verbose_name="因变量", blank=True, null=True, default="", help_text="目标项")
    division_ratio = models.FloatField(verbose_name="数据划分比例", default=0)
    mth_power = models.IntegerField(verbose_name="次数m", default=1)
    error_type = models.IntegerField(choices=ERROR_TYPE, verbose_name="误差计算类别", help_text="默认MSE")
    chart_folder1 = models.CharField(max_length=50, verbose_name="图表存放路径1", null=True, blank=True, default="")
    chart_folder2 = models.CharField(max_length=50, verbose_name="图表存放路径2", null=True, blank=True, default="")
    chart_folder3 = models.CharField(max_length=50, verbose_name="图表存放路径3", null=True, blank=True, default="")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    updated_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "回归分析模型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
