# Generated by Django 2.0.4 on 2018-06-12 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_taskinfo_task_desc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskinfo',
            old_name='state_type',
            new_name='status_type',
        ),
    ]