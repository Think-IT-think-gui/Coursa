# Generated by Django 4.1.3 on 2023-04-25 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Handler', '0008_topic_info_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=1000)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
