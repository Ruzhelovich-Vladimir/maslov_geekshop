from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm


def login(request):
    title = 'вход'
    # Активируем форму аунтентификацию
    login_from = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_from.is_valid():
        username = request.POST.get('username')
        password = request.POST['password']
        # Запускаем аунтентификацию
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            # auth.login пропишет пользователя в объект запроса request.
            auth.login(request, user)
            # возвращает на главную страницу
            return HttpResponseRedirect(reverse('main'))
    content = {'title': title, 'login_form': login_from}
    return render(request, 'authapp/login.html', content)

def logout(request):

    title = 'выход'
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))

def register(request):

    title = 'регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            # Если все хорошо, сохраняем пользователя и переходим на страницу аунтентификации
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        # В противном случае ототажаем форому регистрации и невалидными ошибами
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def edit(request):

    title = 'редактирование профиля'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_from = ShopUserEditForm(instance=request.user)
        content = {'title': title, 'edit_form': edit_from}
        return render(request, 'authapp/edit.html', content)




