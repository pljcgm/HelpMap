# Generated by Django 3.0.6 on 2020-05-13 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='helppoint',
            old_name='map_point',
            new_name='geom',
        ),
    ]