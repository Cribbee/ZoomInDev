from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class TaskInfo(models.Model):
    """
    任务信息
    """
    STATE_TYPE =(
        (0, "已删除"),
        (1, "已完成"),
        (2, "未完成"),
    )

    user = models.ForeignKey(User, models.CASCADE, verbose_name="用户ID")
    task_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="任务名")
    data_num = models.IntegerField(max_length=10, default=1, verbose_name="数据文件数量")
    state_type = models.IntegerField(choices=STATE_TYPE, default=2, verbose_name="任务状态", help_text="任务状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    task_desc = models.CharField(max_length=120, default="", null=True, blank=True, verbose_name="任务描述")
    task_home = models.CharField(max_length=2, verbose_name="任务存放盘", default="D")
    task_folder = models.CharField(max_length=50, verbose_name="任务存放文件夹路径名", default="")  # userid + taskid

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

    task = models.ForeignKey(TaskInfo, models.CASCADE, verbose_name="任务信息")
    step1 = models.CharField(max_length=100, verbose_name="json源文件", default="")
    step2 = models.CharField(max_length=100, verbose_name="csv源文件", default="")
    step3 = models.CharField(max_length=100, verbose_name="预处理源文件", default="")
    step4 = models.CharField(max_length=100, verbose_name="数据挖掘源文件", default="")
    step5 = models.CharField(max_length=100, verbose_name="发布任务源文件", default="")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "数据源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.task_id


