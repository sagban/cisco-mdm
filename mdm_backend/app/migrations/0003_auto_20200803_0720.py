# Generated by Django 3.0.8 on 2020-08-03 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200803_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyprediction',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
