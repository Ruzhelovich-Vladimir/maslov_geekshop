from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, redirect
from mainapp.models import Product, ProductCategory

#######################################################
'''
В качестве первого позиционного аргумента декоратору необходимо передать функцию, 
возвращающую логическое значение. Мы написали лямбда-функцию. 
Если доступ пытается получить не суперпользователь — произойдет переход по адресу, 
который прописали в константе LOGIN_URL.
'''
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.filter(is_active=True).order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    content = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    # Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title': title, 'update_form': user_form}
    return render(request, 'adminapp/user_update.html', content)
class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    # reverse_lazy - отрабатывает когда его вызвали, а не при инициализации класса (аналог yielt)
    success_url = reverse_lazy('admin:users')
    # fields = '__all__'
    form_class = ShopUserRegisterForm

    # Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):

    title = 'пользователи/редактиование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserEditForm(request.POST, request.FILES, instance=edit_user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}

    return render(request, 'adminapp/user_update.html', content)
class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    # reverse_lazy - отрабатывает когда его вызвали, а не при инициализации класса (аналог yielt)
    success_url = reverse_lazy('admin:users')
    # fields = '__all__'
    form_class = ShopUserEditForm

    # Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)
class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    # reverse_lazy - отрабатывает когда его вызвали, а не при инициализации класса (аналог yielt)
    success_url = reverse_lazy('admin:users')

    def delete(self, *args, **kwargs):

        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    #Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/удаление'
        return context

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    # Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context

@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()

    content = {'title': title, 'category_form': category_form}
    return render(request, 'adminapp/category_update.html', content)
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    # reverse_lazy - отрабатывает когда его вызвали, а не при инициализации класса (аналог yielt)
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'
    form_class = ProductEditForm

    #Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):

    title = 'категории/редактирование'
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm(instance=edit_category)

    content = {'title': title, 'category_form': category_form}
    return render(request, 'adminapp/category_update.html', content)
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    # reverse_lazy - отрабатывает когда его вызвали, а не при инициализации класса (аналог yielt)
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'
    form_class = ProductEditForm

    #Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):

    title = 'категории/удаление'
    print("удаление")
    delete_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        delete_category.is_active = False
        delete_category.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {'title': title, 'category_to_delete': delete_category}
    return render(request, 'adminapp/category_delete.html', content)
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    # reverse_lazy - отрабатывает когда его вызвали, а не при инициализации класса (аналог yielt)
    success_url = reverse_lazy('admin:categories')

    def delete(self, *args, **kwargs):

        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    #Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)
class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    products_list = None
    category = None
    # TODO: Реализовать нормальное отображение кнопок на не активных продуктов.
    # Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        if 'pk' in kwargs:
            pk = kwargs['pk']
            self.products_list = Product.objects.filter(category__pk=pk).order_by('name')
            self.category = get_object_or_404(ProductCategory, pk=kwargs['pk'])

        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/список'
        context['category'] = self.category
        if self.products_list:
            context['objects'] = self.products_list

        return context

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {'title': title,
               'form': product_form,
               'category': category
               }

    return render(request, 'adminapp/product_update.html', content)
class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductEditForm
    category = None

    # Получение ссыдки редирект
    def get_success_url(self):
        self.success_url = reverse_lazy(f'admin:products', args=[self.category.pk])
        return self.success_url

    # Передача параметры в форму
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProductCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['initial'] = {'category': self.category}
        return kwargs

    #Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # Требуется объект, т.к. необходимо заполнить по умолчанию на форме
        self.category = get_object_or_404(ProductCategory, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        context['category'] = self.category
        return context

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {'title': title,
               'update_form': edit_form,
               'category': edit_product.category
               }

    return render(request, 'adminapp/product_update.html', content)
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    form_class = ProductEditForm
    category = None

    # Получение ссылки редирект
    def get_success_url(self):
        self.success_url = reverse_lazy(f'admin:products', args=[self.category.pk])
        return self.success_url

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        category_pk = self.get_object().category.pk
        self.category = get_object_or_404(ProductCategory, pk=category_pk)
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/редактирование'
        context['category'] = self.category
        return context

@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/подробнее'
    product = get_object_or_404(Product, pk=pk)
    content = {'title': title, 'object': product,}

    return render(request, 'adminapp/product_read.html', content)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
    category = None

    #Для реализация контроля авторизации, переопредяляем метод dispatch
    # со следующим дикоратором
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        category_pk = self.get_object().category.pk
        self.category = get_object_or_404(ProductCategory, pk=category_pk)
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/подробнее'
        context['category'] = self.category
        return context

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))

    content = {'title': title, 'product_to_delete': product, }

    return render(request, 'adminapp/product_delete.html', content)
class ProductDeleteView(DeleteView):

    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy(f'admin:products')
    category = None

    def get_success_url(self, pk):
        self.success_url = reverse_lazy(f'admin:products', args=[pk])
        return self.success_url

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return redirect(self.get_success_url(pk=self.object.category.pk))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        category_pk = self.get_object().category.pk
        self.category = get_object_or_404(ProductCategory, pk=category_pk)
        return super().dispatch(*args, **kwargs)

    # добавляем контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'продукт/{"удаление" if self.get_object().is_active else "восстановление" }'
        context['category'] = self.category
        return context
