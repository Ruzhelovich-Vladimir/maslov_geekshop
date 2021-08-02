from django.shortcuts import render
import json

def main(request):
    content = {
        'title': 'главная'
    }
    return render(request, 'mainapp/index.html', content)

def products(request):

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

def contact(request):

    with open('contacts.json', 'r') as f:
        contacts = json.load(f)

    content = {
        'title': 'контакты',
        'contacts': contacts
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
