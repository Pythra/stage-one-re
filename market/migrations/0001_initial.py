# Generated by Django 3.0.7 on 2020-09-16 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('tags', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=30)),
                ('LGA', models.CharField(default='', max_length=30)),
                ('area', models.CharField(default='', max_length=30)),
                ('street', models.CharField(default='', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('price', models.IntegerField()),
                ('description', models.TextField(null=True)),
                ('specifications', models.TextField()),
                ('condition', models.CharField(choices=[('bn', 'Brand-new'), ('sh', 'Second-hand')], default='bn', max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('picture', models.ImageField(upload_to='product_pics')),
                ('pic1', models.ImageField(blank=True, null=True, upload_to='product_pics')),
                ('pic2', models.ImageField(blank=True, null=True, upload_to='product_pics')),
                ('pic3', models.ImageField(blank=True, null=True, upload_to='product_pics')),
                ('pic4', models.ImageField(blank=True, null=True, upload_to='product_pics')),
                ('pic5', models.ImageField(blank=True, null=True, upload_to='product_pics')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('category', models.ManyToManyField(to='market.Category')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.Location')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.IntegerField(default=0, null=True)),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('name', models.CharField(max_length=60)),
                ('phone', models.IntegerField(default=234, null=True)),
                ('site', models.URLField(blank=True, null=True)),
                ('establishment_pic', models.ImageField(upload_to='shop_pics')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('charge', models.TextField(max_length=100)),
                ('description', models.TextField()),
                ('experience', models.CharField(max_length=15)),
                ('qualifications', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='service_pics')),
                ('pic1', models.ImageField(blank=True, null=True, upload_to='service_pics')),
                ('pic2', models.ImageField(blank=True, null=True, upload_to='service_pics')),
                ('pic3', models.ImageField(blank=True, null=True, upload_to='service_pics')),
                ('pic4', models.ImageField(blank=True, null=True, upload_to='service_pics')),
                ('pic5', models.ImageField(blank=True, null=True, upload_to='service_pics')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('category', models.ManyToManyField(to='market.Category')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.Location')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Shop')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=18)),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('dp', models.ImageField(null=True, upload_to='review_dp')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='review_pics')),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='review_pics')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='review_pics')),
                ('photo3', models.ImageField(blank=True, null=True, upload_to='review_pics')),
                ('photo4', models.ImageField(blank=True, null=True, upload_to='review_pics')),
                ('photo5', models.ImageField(blank=True, null=True, upload_to='review_pics')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='market.Product')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='market.Service')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('ref_pic', models.ImageField(blank=True, null=True, upload_to='request_pics')),
                ('max_price', models.IntegerField()),
                ('min_price', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Shop')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.Shop'),
        ),
    ]
