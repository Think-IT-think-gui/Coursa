# Generated by Django 4.1.3 on 2023-04-27 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Handler', '0012_topic_info_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module_info',
            name='Name',
        ),
    ]