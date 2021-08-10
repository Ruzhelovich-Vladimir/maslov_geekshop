import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

JSON_PATH = os.path.join(settings.BASE_DIR, 'mainapp', 'json')

def load_json_data(filename):

    with open(os.path.join(JSON_PATH, f'{filename}.json'), 'r') as _f:
        return json.load(_f)

class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_json_data('categories')
        ProductCategory.objects.all().delete()
        for category in categories:
            ProductCategory.objects.create(**category)

        products = load_json_data('products')
        Product.objects.all().delete()
        for product in products:
            product['category'] = ProductCategory.objects.get(name=product['category'])
            Product.objects.create(**product)

        ShopUser.objects.all().delete()
        ShopUser.objects.create_superuser(username='django', email='django@localhost', password='geekbrains', age=46)


