# Generated by Django 2.1.3 on 2018-11-29 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20181126_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='contest',
        ),
    ]
