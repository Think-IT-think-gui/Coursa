# Generated by Django 4.1.3 on 2023-04-27 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Handler', '0013_remove_module_info_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic_info',
            name='Description',
        ),
    ]
