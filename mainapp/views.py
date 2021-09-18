import datetime
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
#from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

# Карзина добавлена в контекстный процессор
# def get_basket(user):
#     #return Basket.objects.filter(user=user) if user.is_authenticated else []
#     return user.basket.all() if user.is_authenticated else []

def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]

def get_same_products(product):
    return Product.objects.filter(category__pk=product.category.pk).exclude(pk=product.pk)[:3]

def main(request):

    content = {
        'title': 'главная',
        'products': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', content)

def get_links_menu():
    title = 'продукты'
    # контент для нулевой категории
    category_0 = {'pk': 0, 'name': 'все'}
    links_menu = list(ProductCategory.objects.all())
    # Добавляем виртуальную категорию
    links_menu.insert(0, category_0)
    return links_menu


def products(request, pk=None, page=1):

    title = 'продукты'
    category_0 = {'pk': 0, 'name': 'все'}
    links_menu = get_links_menu()
    # basket = get_basket(user=request.user)

    # Если мы работаем с подменю
    if pk is not None:
        if pk == 0:
            category = category_0
            product_list = Product.objects.all()
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_list = Product.objects.filter(category__pk=category.pk)

        # Объект пагинатор, "2" - кол-во товаров на странице
        paginator = Paginator(product_list, 6)
        try:
            # Попытка получить страницу
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            # Если ошибка не число, то переход на первую страницу
            product_paginator = paginator.page(1)
        except EmptyPage:
            # Если пустая страницаошибка не число, то переход на первую страницу
            product_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': product_paginator,
            'category': category,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product}

    #print(same_products)

    return render(request, 'mainapp/products.html', content)

def product(request, pk):

    title = 'продукты'

    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', content)


def contact(request):

    title = 'о нас'
    visit_date = datetime.datetime.now()

    locations = [
        {
            'city': 'Москва',
            'phone': '+7 800 888 88 88',
            'email': 'info@geekshop.ru',
            'address': 'в пределах МКАД'
         },
        {
            'city': 'Екатеринбур',
            'phone': '+7 800 888 88 88',
            'email': 'info@geekshop.ru',
            'address': 'в центре'
        },
        {
            'city': 'Владивосток',
            'phone': '+7 800 888 88 88',
            'email': 'info@geekshop.ru',
            'address': 'прибрежная зона'
        }
    ]
    content = {
        'title': title, 'visit_date': visit_date, 'locations': locations
    }

    return render(request, 'mainapp/contact.html', content)

def not_found(request, exception):
    # контроллер кастомной обработки ошибки
    # необходтмо также прописать с диспетчере урлов на данный контроллер
    # handler404 = 'mainapp.views.not_found'
    return render(request=request, template_name='404.html', context={'item': 'item'}, status=404)




