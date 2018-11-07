from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from tasks.models import TaskInfo
# Create your models here.
User = get_user_model()


class UserTask(models.Model):
    """
    用户收藏任务
    """
    user = models.ForeignKey(User, models.CASCADE, null=True, verbose_name="用户", )
    tasks = models.ForeignKey(TaskInfo, models.CASCADE, verbose_name="任务", help_text="任务id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        #联合字段构成唯一集合，避免重复收藏
        unique_together = ("user", "tasks")

    def __str__(self):
        return self.user.username


class Publish(models.Model):
    """
    用户发布任务
    """

    user = models.ForeignKey(User, models.CASCADE, null=True, verbose_name="分享者用户", related_name="user")
    shared_user = models.IntegerField(null=True, verbose_name="被分享者用户")
    source_task = models.ForeignKey(TaskInfo, models.CASCADE, verbose_name="源任务", help_text="源任务id")
    task = models.IntegerField(null=True, blank=True, verbose_name="分享后的任务id", help_text="分享后的任务id")
    task_name = models.CharField(max_length=80, null=True, blank=True, verbose_name="分享任务名", help_text="分享任务名")
    add_time = models.DateTimeField(null=True, blank=True, default=datetime.now, verbose_name=u"添加时间")
    update_time = models.DateTimeField(null=True, blank=True, default=datetime.now, verbose_name=u"更新时间")

    class Meta:
        verbose_name = '发布'
        verbose_name_plural = verbose_name
        #联合字段构成唯一集合，避免重复收藏
        unique_together = ("user", "task_name")

    def __str__(self):
        return self.task_name

