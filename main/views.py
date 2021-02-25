from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import *
from .mixins import CategoryDetailMixin
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from orders.models import Order, OrderItem

from django.views import View
from django.core.mail import send_mail

from main.filters import ProductFilter
import django_filters
import re


class BaseView(View):
    """Базовое представление"""

    def get(self, request, *args, **kwargs):
        # categories = CategoryProduct.objects.get_categories_for_left_sidebar()
        # ИСПРАВИТЬ!!!!!!!!!!!!!
        categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                      {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
        # products = LatestProducts.objects.get_products_for_main_page('iphone', 'ipad')
        products = Product.objects.all()
        search_iphone_diagonal = re.findall("'(.+?)'", str(set(Iphone.objects.values_list('diagonal'))))
        search_ipad_diagonal = re.findall("'(.+?)'", str(set(Ipad.objects.values_list('diagonal'))))
        filter_result_diagonal = search_iphone_diagonal + search_ipad_diagonal

        filter = ProductFilter(request.GET, queryset=products)

        context = {
            'categories': categories,
            'products': products,
            'test': filter_result_diagonal,
            'filter': filter,
        }
        return render(request, 'main/base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):
    """Класс для отобраения порбродной информации для выбранного товара"""
    # CT_MODEL_CLASS = {
    #     'iphone': Iphone,
    #     'ipad': Ipad
    # }
    #
    # def dispatch(self, request, *args, **kwargs):
    #     """ Возвращаем выбранную пользователем модель товара """
    #     self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
    #     self.queryset = self.model._base_manager.all()
    #     return super(ProductDetailView, self).dispatch(request, *args, **kwargs)
    model = Product
    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):
    """Класс для оторбажения товаров, относящихся к определенной категории"""

    model = CategoryProduct
    queryset = CategoryProduct.objects.all()
    context_object_name = 'category'
    template_name = 'main/category_detail.html'
    slug_url_kwarg = 'slug'


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        # categories = CategoryProduct.objects.all()
        categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                      {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
        context = {'form': form, 'categories': categories}
        return render(request, 'main/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'main/login.html', {'form': form})


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        # categories = CategoryProduct.objects.all()
        categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                      {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
        context = {'form': form, 'categories': categories}
        return render(request, 'main/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, 'main/registration.html', {'form': form})


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        # customer = Customer.objects.get(user=request.user.phone)
        customer = request.user
        # categories = CategoryProduct.objects.all()
        categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                      {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
        products = Product.objects.all()
        test = OrderItem.objects.all()
        orders = Order.objects.filter(email=customer.email).order_by('-created')
        return render(request, 'main/profile.html',
                      {'orders': orders, 'products': products, 'quantity': test, 'categories': categories})


# class EContactsView(View):
#     # template_name = 'main/contacts_info.html'
#     def get(self, request, *args, **kwargs):
#         categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
#                       {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
#         return render(request, 'main/contacts_info.html', {'categories': categories})


def contact(request):
    categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                  {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']
        # categories = CategoryProduct.objects.all()

        send_mail(
            message_name,
            message,
            message_email,  # на какой емейл
            ['zakaraya2000@mail.ru']  # с какого емейла
        )

        return render(request, 'main/contacts_info.html', {'message_name': message_name, 'categories': categories})
    else:
        return render(request, 'main/contacts_info.html', {'categories': categories})


def product_list(request, pk):
    if pk == 1:
        filter = Product.objects.all()
    elif pk == 2:
        filter = Product.objects.filter(available=True).order_by('price')
    else:
        filter = Product.objects.filter(available=True).order_by('-price')
    return render(request, 'main/sorting.html', {'products': filter})


def film_list(request):
    films = Product.objects.all()
    filter = ProductFilter(request.GET, queryset=films)
    return render(request, 'main/filters.html', {'filter': filter})
