from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser


def send_verify_email(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = f'подтверждение учётной записи {user.username}'

    message = f'Для подтверждения перейдите по ссылке: {settings.DOMAIN}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):

    print(email, activation_key)
    try:
        user = get_object_or_404(ShopUser, email=email, activation_key=activation_key)
        if not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
    except Exception as ex:
        return HttpResponseRedirect(reverse('main'))


def login(request):
    title = 'вход'
    # Активируем форму аунтентификацию
    login_from = ShopUserLoginForm(data=request.POST)
    # Забираем параметр по ключу, для страницы обратного перехода
    next_url = request.GET.get('next', '')
    if request.method == 'POST' and login_from.is_valid():
        username = request.POST.get('username')
        password = request.POST['password']
        # Запускаем аунтентификацию
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            # auth.login пропишет пользователя в объект запроса request.
            auth.login(request, user)
            #Если 'next' был в запросе POST
            if 'next' in request.POST.keys():
                # Возвращаем пользователя на страницу по ключу "next"
                return HttpResponseRedirect(request.POST['next'])
            # возвращает на главную страницу
            return HttpResponseRedirect(reverse('main'))
    content = {'title': title, 'login_form': login_from, 'next': next_url}
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
            user = register_form.save()
            send_verify_email(user=user)
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




