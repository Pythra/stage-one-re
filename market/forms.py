from django.forms import Textarea, TextInput, NumberInput, FileInput
from .models import Product, Shop, Service, Review, Request
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'condition', 'pic1', 'pic2', 'pic3', 'pic4', 'pic5')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'pic1': FileInput(attrs={'class': 'form-control'}),
            'pic2': FileInput(attrs={'class': 'form-control'}),
            'pic3': FileInput(attrs={'class': 'form-control'}),
            'pic4': FileInput(attrs={'class': 'form-control'}),
            'pic5': FileInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'describe the product'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'charge', 'description', 'picture', 'experience', 'qualifications', 'pic1', 'pic2', 'pic3', 'pic4', 'pic5')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'charge': NumberInput(attrs={'class': 'form-control',}),
            'pic1': FileInput(),
            'pic2': FileInput(),
            'pic3': FileInput(),
            'pic4': FileInput(),
            'pic5': FileInput(),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'describe the product'}),
            'experience': TextInput(attrs={'class': 'form-control'}),
            'qualifications': TextInput(attrs={'class': 'form-control'}),
        }


class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ('name', 'location', 'establishment_pic')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of your buisness'}),
            'establishment_pic': FileInput(),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'content', 'photo', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'}),
            'photo1': FileInput(),
            'photo2': FileInput(),
            'photo3': FileInput(),
            'photo4': FileInput(),
            'photo5': FileInput(),
                   }


class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ('title', 'description', 'ref_pic', 'min_price', 'max_price')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'What do you need?'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': "Describe what you're looking for"}),
            'min_price': NumberInput(attrs={'class': 'form-control'}),
            'max_price': NumberInput(attrs={'class': 'form-control'}),
            'ref_pic': FileInput(),
        }


