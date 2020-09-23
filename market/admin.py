from django.contrib import admin

# Register your models here.
from .models import Product, Service, Shop, Category, Location, Review, Request


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'charge')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category)

admin.site.register(Location)
admin.site.register(Review)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_price', 'max_price', 'description')
    search_fields = ('title',)

