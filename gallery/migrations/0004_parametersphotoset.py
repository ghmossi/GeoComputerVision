# Generated by Django 3.2.19 on 2023-08-03 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_streetobject_objtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParametersPhotoSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countLuminaria', models.IntegerField()),
                ('countPostacion', models.IntegerField()),
                ('countVehiculos', models.IntegerField()),
                ('countOtros', models.IntegerField()),
                ('lastPhotoDetect', models.IntegerField()),
                ('photoset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albumParamters', to='gallery.photoset')),
            ],
        ),
    ]