from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from tasks.models import TaskInfo
# Create your models here.
User = get_user_model()


class UserTask(models.Model):
    """
    用户操作任务
    """
    user = models.ForeignKey(User, models.CASCADE, verbose_name="用户", )
    tasks = models.ForeignKey(TaskInfo, models.CASCADE, verbose_name="任务", help_text="任务id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        unique_together = ("user", "tasks")

    def __str__(self):
        return self.user.username