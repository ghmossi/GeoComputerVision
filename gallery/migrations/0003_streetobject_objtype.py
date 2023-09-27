# Generated by Django 4.2.2 on 2023-07-11 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_alter_streetobject_roi_objectattributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='streetobject',
            name='objtype',
            field=models.CharField(choices=[('postacion', 'Postacion'), ('luminaria', 'Luminaria'), ('vehiculo', 'Vehiculo'), ('otros', 'Otros')], default='otros', max_length=20, null=True),
        ),
    ]
