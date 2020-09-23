from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .forms import ProductForm, ShopForm, ServiceForm, ReviewForm, RequestForm
from .models import Product, Service, Shop, Review, Request


def market_index(request):
    if request.user.is_authenticated:
        area_products = Product.objects.filter(location__area=request.user.shop.location.area).order_by(
                            '-created_on')[:36]
        area_services = Service.objects.filter(location__area=request.user.shop.location.area).order_by(
                            '-created_on')[:36]

        state_products = Product.objects.filter(location__state=request.user.shop.location.state
                                                ).exclude(location__area=request.user.shop.location.area
                                                          ).order_by('-created_on')[:12]
        state_services = Service.objects.filter(location__state=request.user.shop.location.state
                                                ).exclude(location__area=request.user.shop.location.area
                                                          ).order_by('-created_on')[:12]

        country_products = Product.objects.filter(location__state=request.user.shop.location.country
                                                ).exclude(location__state=request.user.shop.location.state
                                                          ).order_by('-created_on')[:12]
        country_services = Service.objects.filter(location__state=request.user.shop.location.country
                                                ).exclude(location__state=request.user.shop.location.state
                                                          ).order_by('-created_on')[:12]
        new_shops = Shop.objects.order_by('-created_on')[:6]
        requests = Request.objects.order_by('-created_on')
        context = {
                'area_products': area_products,
                'area_services': area_services,
                'state_products': state_products,
                'state_services': state_services,
                'country_products': country_products,
                'country_services': country_services,
                'new_shops': new_shops,
                'requests': requests,
                    }
        return render(request, 'market/market_home.html', context)
    else:
        all_products = Product.objects.all()
        all_services = Service.objects.all()
        requests = Request.objects.order_by('-created_on')
        context = {
                'all_products': all_products,
                'all_services': all_services,
                'requests': requests,
                    }
        return render(request, 'market/stranger_home.html', context)


def product_detail(request, slug):
    template_name = 'market/product_detail.html'
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all
    context = {'product': product, 'slug': slug, 'reviews': reviews}
    return render(request, template_name, context)


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('market_home')
    template_name = 'market/my_shop.html'


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.location = request.user.shop.location
            product.shop = request.user.shop
            product.save()
            return HttpResponseRedirect(reverse('market_home'))
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'market/product_form.html', context)


def service_detail(request, slug):
    template_name = 'market/service_detail.html'
    service = get_object_or_404(Service, slug=slug)
    reviews = service.reviews.all
    context = {'service': service, 'slug': slug, 'reviews': reviews}
    return render(request, template_name, context)


class ServiceUpdate(UpdateView):
    model = Service
    form_class = ServiceForm


class ServiceDelete(DeleteView):
    model = Service
    success_url = reverse_lazy('market_home')


@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.location = request.user.shop.location
            service.shop = request.user.shop
            service.save()
            return HttpResponseRedirect(reverse('market_home'))
    else:
        form = ServiceForm()
    context = {'form': form}
    return render(request, 'market/service_form.html', context)


@login_required
def my_shop(request):
    my_services = request.user.shop.service_set.all
    my_products = request.user.shop.product_set.all
    if request.method == 'POST':
        profile_form = ShopForm(request.POST, request.FILES, instance=request.user.shop)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return HttpResponseRedirect(reverse('shop', kwargs={'pk': request.user.id}))

    else:
        profile_form = ShopForm(instance=request.user.shop)

    context = {'p_form': profile_form, 'my_products': my_products, 'my_services': my_services}
    return render(request, 'market/my_shop.html', context)


@login_required
def visit_shop(request, pk):
    user = User.objects.get(pk=pk)
    services = user.shop.service_set.all
    products = user.shop.product_set.all
    context = {'user': user, 'products': products, 'services': services}
    return render(request, 'market/visit_shop.html', context)


class ShopUpdate(UpdateView):
    model = Shop
    form_class = ShopForm


class ShopDelete(DeleteView):
    model = Shop
    success_url = reverse_lazy('market_home')


@login_required
def review_create(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = request.user
            review.dp = request.user.shop.establishment_pic.url
            review.save()
            return HttpResponseRedirect(reverse('product_detail', kwargs={'slug': slug}))
    else:
        form = ReviewForm()
    context = {'form': form, 'product': product}
    return render(request, 'market/review_form.html', context)


class ReviewUpdate(UpdateView):
    model = Review
    form_class = ReviewForm


class ReviewDelete(DeleteView):
    model = Review
    success_url = reverse_lazy('product_detail')


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    services = Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context = {'products': products, 'services': services}
    return render(request, 'market/search/search_home.html', context)


def all_area_products(request):
    products = Product.objects.filter(location__area=request.user.shop.location.area).order_by('-created_on')
    context = {'products': products}
    return render(request, 'market/list_all/all_area_products.html', context)


def all_area_services(request):
    services = Service.objects.filter(location__area=request.user.shop.location.area).order_by('-created_on')
    context = {'services': services}
    return render(request, 'market/list_all/all_area_services.html', context)


def all_state_products(request):
    state_products = Product.objects.filter(location__state=request.user.shop.location.state).order_by('-created_on')
    context = {'state_products': state_products}
    return render(request, 'market/list_all/all_state_products.html', context)


def all_state_services(request):
    state_services = Service.objects.filter(location__state=request.user.shop.location.state).order_by('-created_on')
    context = {'state_services': state_services}
    return render(request, 'market/list_all/all_state_services.html', context)


def all_area_shops(request):
    shops = Shop.objects.filter(location__area=request.user.shop.location.area).order_by('-created_on')
    context = {'shops': shops}
    return render(request, 'market/list_all/all_area_shops.html', context)


def all_state_shops(request):
    shops = Shop.objects.filter(location__state=request.user.shop.location.state).order_by('-created_on')
    context = {'shops': shops}
    return render(request, 'market/list_all/all_state_shops.html', context)


@login_required
def request_create(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            req = form.save(commit=False)
            req.shop = request.user.shop
            req.save()
            return HttpResponseRedirect(reverse('market_home'))
    else:
        form = RequestForm()
    context = {'form': form}
    return render(request, 'market/request_form.html', context)


def request_detail(request, pk):
    template_name = 'market/request_detail.html'
    req = get_object_or_404(Request, pk=pk)
    context = { 'req': req}
    return render(request, template_name, context)


def settings(request):
    template_name = 'market/settings.html'
    return render(request, template_name)

