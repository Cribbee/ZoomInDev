# Generated by Django 2.0.4 on 2018-09-07 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='task_num',
            field=models.IntegerField(default=0, null=True, verbose_name='任务数量'),
        ),
    ]