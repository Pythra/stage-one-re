# Generated by Django 3.0.7 on 2020-09-16 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='product',
            name='specifications',
        ),
    ]
