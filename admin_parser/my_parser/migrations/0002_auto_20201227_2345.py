# Generated by Django 3.1.4 on 2020-12-27 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_parser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=20, verbose_name='Title'),
        ),
    ]