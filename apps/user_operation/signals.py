# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 5

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


from user_operation.models import UserTask


@receiver(post_save, sender=UserTask)
def create_usertask(sender, instance=None, created=False, **kwargs):
    if created:
        tasks = instance.tasks
        tasks.create_num += 1
        tasks.save()


@receiver(post_delete, sender=UserTask)
def delete_usertask(sender, instance=None, created=False, **kwargs):
    tasks = instance.tasks
    tasks.create_num -= 1
    tasks.save()