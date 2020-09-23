# Generated by Django 3.0.7 on 2020-09-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_auto_20200916_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='picture',
        ),
        migrations.AlterField(
            model_name='product',
            name='pic1',
            field=models.ImageField(default='smileboy.jpg', upload_to='product_pics'),
            preserve_default=False,
        ),
    ]
