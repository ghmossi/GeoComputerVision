# Generated by Django 3.2.19 on 2023-10-23 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_parametersphotoset_statusdetection'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametersphotoset',
            name='tasksId',
            field=models.CharField(max_length=200, null=True),
        ),
    ]