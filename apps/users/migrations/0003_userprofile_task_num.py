# Generated by Django 2.0.4 on 2018-05-30 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180411_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='task_num',
            field=models.IntegerField(default=0, max_length=10, null=True, verbose_name='任务数量'),
        ),
    ]
