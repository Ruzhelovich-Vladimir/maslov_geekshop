from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def main(request):

    products = Product.objects.all()[:4]
    content = {
        'title': 'главная',
        'products': products
    }
    return render(request, 'mainapp/index.html', content)

def products(request, pk=None):

    links_menu = ProductCategory.objects.all()

    content = {
        'title': 'продукты',
        'links_menu': links_menu,
        'same_products': []
    }
    return render(request, 'mainapp/products.html', content)

def category(request):
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
