from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product

def __get_basket_html_JsonResponse(request):
    # Получаю карзины всех товаров
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    content = {
        'basket_items': basket_items
    }
    # Получаю html код на основне подшаблона в ввиде сроки
    result = render_to_string('basketapp/includes/inc_basket_list.html', content)
    # print(result)
    # возврат лучше делать в json-формате
    return JsonResponse({'result': result})


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    content = {
        'title': title,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def add(request, pk):
    # Если добавляется товар со странице login,
    # то отправляем пользователя на страницу товара.
    # Все зависит от техического задания.
    # Этот код решает проблемы зацикливания, если не авторизаванный
    # пользователь добавит товар.
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    #######################################################################
    product = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(user=request.user, product=product).first()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product)
    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete(request, pk):
    # Если запрос ajax?
    if request.is_ajax():
        # Получаю карзину по продукту
        basket_item = Basket.objects.get(pk=pk)
        basket_item.delete()
        # Возвращщаем json разметку для ajax-запроса
        return __get_basket_html_JsonResponse(request)

    # basket_item = get_object_or_404(Basket, pk=pk)
    # basket_item.delete()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edit(request, pk, quantity):
    # Если запрос ajax?
    if request.is_ajax():
        # На всякий случай преобразую в int
        quantity = int(quantity)
        # Получаю карзину по продукту
        new_basket_item = Basket.objects.get(pk=pk)
        # Если кол-во больше 0
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        # Возвращщаем json разметку для ajax-запроса
        return __get_basket_html_JsonResponse(request)
