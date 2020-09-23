from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

CONDITION = (
    ('bn', "Brand-new"),
    ('sh', "Second-hand")
)


class Category(models.Model):
    name = models.CharField(max_length=20)
    tags = models.TextField()


class Location(models.Model):
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=30)
    LGA = models.CharField(max_length=30, default='')
    area = models.CharField(max_length=30, default='')
    street = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.area


class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)
    sales = models.IntegerField(default=0, null=True)
    rating = models.DecimalField(max_digits=5, default=0, decimal_places=1)
    name = models.CharField(max_length=60, )
    phone = models.IntegerField(default=234, null=True)
    site = models.URLField(null=True, blank=True)
    establishment_pic = models.ImageField(upload_to='shop_pics')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Shop(user=user)
        profile.save()


class Product(models.Model):
    name = models.CharField(max_length=60)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    description = models.TextField(null=True)
    condition = models.CharField(max_length=20, choices=CONDITION, default='bn')
    quantity = models.IntegerField(default=0)
    pic1 = models.ImageField(upload_to='product_pics')
    pic2 = models.ImageField(upload_to='product_pics', null=True, blank=True)
    pic3 = models.ImageField(upload_to='product_pics', null=True, blank=True)
    pic4 = models.ImageField(upload_to='product_pics', null=True, blank=True)
    pic5 = models.ImageField(upload_to='product_pics', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + self.description)
        super(Product, self).save(*args, **kwargs)


class Service(models.Model):
    name = models.CharField(max_length=60)
    category = models.ManyToManyField(Category)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    charge = models.TextField(max_length=100)
    description = models.TextField()
    experience = models.CharField(max_length=15)
    qualifications = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    picture = models.ImageField(upload_to='service_pics', null=True, blank=True)
    pic1 = models.ImageField(upload_to='service_pics', null=True, blank=True)
    pic2 = models.ImageField(upload_to='service_pics', null=True, blank=True)
    pic3 = models.ImageField(upload_to='service_pics', null=True, blank=True)
    pic4 = models.ImageField(upload_to='service_pics', null=True, blank=True)
    pic5 = models.ImageField(upload_to='service_pics', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    customer = models.CharField(max_length=18)
    title = models.CharField(max_length=20)
    content = models.TextField()
    dp = models.ImageField(upload_to="review_dp", null=True)
    photo = models.ImageField(upload_to='review_pics', null=True, blank=True)
    photo1 = models.ImageField(upload_to='review_pics', null=True, blank=True)
    photo2 = models.ImageField(upload_to='review_pics', null=True, blank=True)
    photo3 = models.ImageField(upload_to='review_pics', null=True, blank=True)
    photo4 = models.ImageField(upload_to='review_pics', null=True, blank=True)
    photo5 = models.ImageField(upload_to='review_pics', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('review_detail', args=[self.slug])


class Request(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.TextField()
    ref_pic = models.ImageField(upload_to='request_pics', null=True, blank=True)
    max_price = models.IntegerField()
    min_price = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

