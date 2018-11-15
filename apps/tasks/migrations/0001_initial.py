# Generated by Django 2.0 on 2018-11-15 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_set', models.IntegerField(default=-1, verbose_name='数据集ID')),
                ('title', models.CharField(default='', help_text='图表标题', max_length=20, verbose_name='图表标题')),
                ('desc', models.CharField(blank=True, default='', help_text='图表描述', max_length=20, null=True, verbose_name='图表描述')),
                ('chart_type', models.IntegerField(choices=[(1, '簇状直方图'), (2, '折线图'), (3, '普通饼图'), (4, '散点图')], help_text='表格类别', verbose_name='表格类别总览')),
                ('chart_method', models.CharField(default='', help_text='数据处理方法', max_length=200, verbose_name='数据处理方法总揽')),
                ('sort', models.IntegerField(default=-1, help_text='表格排序方式', verbose_name='排序方式')),
                ('sort_value', models.CharField(blank=True, default='', help_text='图表排序基准', max_length=20, null=True, verbose_name='排序基准')),
                ('filter_past_logical_type', models.CharField(blank=True, default='', help_text='图表筛选逻辑', max_length=20, null=True, verbose_name='筛选条件逻辑')),
                ('filter', models.CharField(blank=True, default='', help_text='图表筛选条件', max_length=500, null=True, verbose_name='筛选条件')),
                ('filter_past', models.CharField(blank=True, default='', help_text='图表处理前筛选条件', max_length=500, null=True, verbose_name='处理前筛选条件')),
                ('x_axis', models.CharField(blank=True, default='', help_text='图表维度', max_length=200, null=True, verbose_name='维度')),
                ('y_axis', models.CharField(blank=True, default='', help_text='图表数值', max_length=200, null=True, verbose_name='数值')),
                ('contrast_axis', models.CharField(blank=True, default='', help_text='图表对比轴', max_length=200, null=True, verbose_name='对比')),
                ('secondary_axis', models.CharField(blank=True, default='', help_text='图表次轴', max_length=200, null=True, verbose_name='次轴')),
                ('chart_type_2nd', models.IntegerField(choices=[(1, '簇状直方图'), (2, '折线图'), (3, '普通饼图'), (4, '散点图')], default=1, help_text='次轴表格类别', verbose_name='表格次轴总览')),
                ('chart_method_2nd', models.CharField(default='', help_text='次轴数据处理方法', max_length=200, verbose_name='次轴数据处理方法总揽')),
                ('chart_folder1', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='图表存放路径1')),
                ('chart_folder2', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='图表存放路径2')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '数据图表',
                'verbose_name_plural': '数据图表',
            },
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', help_text='标题', max_length=20, verbose_name='数据集文件名')),
                ('desc', models.CharField(default='', help_text='数据集描述描述', max_length=20, verbose_name='数据集描述信息')),
                ('step1', models.CharField(default='', max_length=100, verbose_name='json源文件名')),
                ('step2', models.CharField(default='', max_length=100, verbose_name='csv源文件名')),
                ('step3', models.CharField(default='', max_length=100, verbose_name='预处理源文件')),
                ('step4', models.CharField(default='', max_length=100, verbose_name='数据挖掘源文件')),
                ('step5', models.CharField(default='', max_length=100, verbose_name='发布任务源文件')),
                ('stepX1', models.CharField(default='', max_length=100, verbose_name='数据集属性文件')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '数据源',
                'verbose_name_plural': '数据源',
            },
        ),
        migrations.CreateModel(
            name='TaskInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(blank=True, help_text='任务名', max_length=30, null=True, verbose_name='任务名')),
                ('data_num', models.IntegerField(default=0, verbose_name='数据文件数量')),
                ('status_type', models.IntegerField(choices=[(0, '已删除'), (1, '已完成'), (2, '未完成')], default=2, help_text='任务状态', verbose_name='任务状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('task_desc', models.CharField(blank=True, default='', help_text='任务描述', max_length=120, null=True, verbose_name='任务描述')),
                ('task_home', models.CharField(default='D', max_length=2, verbose_name='任务存放盘')),
                ('task_folder', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='任务存放文件夹路径')),
            ],
            options={
                'verbose_name': '任务信息',
                'verbose_name_plural': '任务信息',
            },
        ),
    ]
