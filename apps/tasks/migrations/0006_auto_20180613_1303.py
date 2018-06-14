# Generated by Django 2.0.4 on 2018-06-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20180613_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='chart_type',
            field=models.IntegerField(default=0, help_text='表格类别总览', max_length=10, verbose_name='表格类别总览'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='x_axis',
            field=models.CharField(default='', help_text='维度', max_length=100, verbose_name='维度'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='y_axis',
            field=models.CharField(default='', help_text='数值', max_length=100, verbose_name='数值'),
        ),
    ]
