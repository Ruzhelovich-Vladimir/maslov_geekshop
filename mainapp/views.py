from django.db.models import Sum
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

def main(request):

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        qty = basket.aggregate(Sum('quantity'))['quantity__sum']

    content = {
        'title': 'главная',
        'products': Product.objects.all()[:4],
        'qty': qty
    }

    return render(request, 'mainapp/index.html', content)

def products(request, pk=None):

    title = 'продукты'
    summa = 0
    # контент для нулевой категории
    category_0 = {'pk': 0, 'name': 'все'}
    links_menu = list(ProductCategory.objects.all())
    # Добавляем виртуальную категорию
    links_menu.insert(0, category_0)

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        qty = Basket.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']

    # Если мы работаем с подменю
    if pk is not None:
        if pk == 0:
            category = category_0
            product_list = Product.objects.all()
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_list = Product.objects.filter(category__pk=category.pk)
        content = {
            'title': title,
            'links_menu': links_menu,
            'products': product_list,
            'category': category,
            'basket': basket,
            'qty': qty
        }
        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()[3:5]
    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'qty': qty}

    return render(request, 'mainapp/products.html', content)

def category(request):
    content = {}
    return render(request, 'mainapp/category.html', content)

def contact(request):
    content = {
        'title': 'контакты'
    }
    return render(request, 'mainapp/contact.html', content)

def products_all(request):

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)

def products_home(request):

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)

def products_office(request):

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)

def products_modern(request):

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)

def products_classic(request):

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)
