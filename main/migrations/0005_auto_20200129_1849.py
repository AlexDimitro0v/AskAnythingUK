# Generated by Django 2.1.11 on 2020-01-29 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_purchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialism',
            name='category',
        ),
        migrations.RemoveField(
            model_name='specialism',
            name='feedback',
        ),
        migrations.DeleteModel(
            name='Specialism',
        ),
    ]