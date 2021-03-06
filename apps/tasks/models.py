from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class TaskInfo(models.Model):
    """
    任务信息
    """
    STATUS_TYPE =(
        (0, "已删除"),
        (1, "已完成"),
        (2, "未完成"),
    )

    user = models.ForeignKey(User, models.CASCADE, null=True, verbose_name="用户ID")
    task_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="任务名", help_text="任务名")
    data_num = models.IntegerField(default=0, verbose_name="数据文件数量")
    status_type = models.IntegerField(choices=STATUS_TYPE, default=2, verbose_name="任务状态", help_text="任务状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    task_desc = models.CharField(max_length=120, default="", null=True, blank=True, verbose_name="任务描述", help_text="任务描述")
    task_home = models.CharField(max_length=2, verbose_name="任务存放盘", default="D")
    task_folder = models.CharField(max_length=50, verbose_name="任务存放文件夹路径", null=True, blank=True, default="")  # userid + taskid

    class Meta:
        verbose_name = "任务信息"
        verbose_name_plural = verbose_name


# str__(self)这个方法定义了当object调用str()时应该返回的值。
    def __str__(self):
        return self.task_name


class DataSet(models.Model):
    """
    数据集信息
    """

    user = models.ForeignKey(User, models.CASCADE, null=True, verbose_name="用户ID")
    task = models.ForeignKey(TaskInfo, models.CASCADE, null=True, verbose_name="任务ID")
    title = models.CharField(max_length=20, verbose_name="数据集文件名", default="", help_text="标题")
    desc = models.CharField(max_length=20, verbose_name="数据集描述信息", default="", help_text="数据集描述描述")
    step1 = models.CharField(max_length=100, verbose_name="json源文件名", default="")
    step2 = models.CharField(max_length=100, verbose_name="csv源文件名", default="")
    step3 = models.CharField(max_length=100, verbose_name="预处理源文件", default="")
    step4 = models.CharField(max_length=100, verbose_name="数据挖掘源文件", default="")
    step5 = models.CharField(max_length=100, verbose_name="发布任务源文件", default="")
    stepX1 = models.CharField(max_length=100, verbose_name="数据集属性文件", default="")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "数据源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Chart(models.Model):
    """
    数据图表信息
    """
    CHART_TYPE = (
        (1, "簇状直方图"),
        (2, "折线图"),
        (3, "普通饼图"),
        (4, "散点图"),
    )

    user = models.ForeignKey(User, models.CASCADE, null=True, verbose_name="用户ID")
    data_set = models.IntegerField(verbose_name="数据集ID", default=-1)
    title = models.CharField(max_length=20, verbose_name="图表标题", default="", help_text="图表标题")
    desc = models.CharField(max_length=20, verbose_name="图表描述", blank=True, null=True, default="", help_text="图表描述")
    chart_type = models.IntegerField(choices=CHART_TYPE, verbose_name="表格类别总览", help_text="表格类别")
    chart_method = models.CharField(max_length=200,verbose_name="数据处理方法总揽",default="",help_text="数据处理方法")
    sort = models.IntegerField(verbose_name="排序方式", help_text="表格排序方式", default=-1)
    sort_value = models.CharField(max_length=20, verbose_name="排序基准", blank=True, null=True, default="",
                                  help_text="图表排序基准")
    filter_past_logical_type = models.CharField(max_length=20,verbose_name="筛选条件逻辑",default="",blank=True,null=True,help_text="图表筛选逻辑")
    filter = models.CharField(max_length=500,verbose_name="筛选条件",default="",blank = True,null=True,help_text="图表筛选条件")
    filter_past = models.CharField(max_length=500,verbose_name="处理前筛选条件",default="",blank = True,null=True,help_text="图表处理前筛选条件")

    x_axis = models.CharField(max_length=200, verbose_name="维度", blank=True, null=True, default="", help_text="图表维度")
    y_axis = models.CharField(max_length=200, verbose_name="数值", blank=True, null=True, default="", help_text="图表数值")
    contrast_axis = models.CharField(max_length=200, verbose_name="对比", blank=True, null=True, default="", help_text="图表对比轴")
    secondary_axis = models.CharField(max_length=200, verbose_name="次轴", blank=True, null=True, default="", help_text="图表次轴")
    chart_type_2nd = models.IntegerField(choices = CHART_TYPE,default=1,verbose_name="表格次轴总览",help_text="次轴表格类别")
    chart_method_2nd = models.CharField(max_length=200,verbose_name="次轴数据处理方法总揽",default="",help_text="次轴数据处理方法")
    chart_folder1 = models.CharField(max_length=50, verbose_name="图表存放路径1", null=True, blank=True, default="")
    chart_folder2 = models.CharField(max_length=50, verbose_name="图表存放路径2", null=True, blank=True, default="")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    updated_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "数据图表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


