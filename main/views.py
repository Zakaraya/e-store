from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import *
from .mixins import CategoryDetailMixin
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from orders.models import Order

from django.views import View
from django.core.mail import send_mail

# from .forms import ContactForm

class BaseView(View):
    """Базовое представление"""

    def get(self, request, *args, **kwargs):
        # categories = CategoryProduct.objects.get_categories_for_left_sidebar()
        # ИСПРАВИТЬ!!!!!!!!!!!!!
        categories = [{'name': 'Айпады', 'url': '/category/ipads/', 'count': 2},
                      {'name': 'Айфоны', 'url': '/category/iphones/', 'count': 2}]
        products = LatestProducts.objects.get_products_for_main_page('iphone', 'ipad')
        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'main/base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):
    """Класс для отобраения порбродной информации для выбранного товара"""
    CT_MODEL_CLASS = {
        'iphone': Iphone,
        'ipad': Ipad
    }

    def dispatch(self, request, *args, **kwargs):
        """ Возвращаем выбранную пользователем модель товара """
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'


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
        categories = CategoryProduct.objects.all()
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
        categories = CategoryProduct.objects.all()
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
        customer = Customer.objects.get(user=request.user)
        categories = CategoryProduct.objects.all()
        orders = Order.objects.filter(customer=customer).order_by('-created')
        return render(request, 'main/profile.html', {'orders': orders, 'categories': categories})


class EContactsView(View):
    template_name = 'main/contacts_info.html'

    # # В случае get запроса, мы будем отправлять просто страницу с контактной формой
    # def get(self, request, *args, **kwargs):
    #     context = {'contact_form': ContactForm()}
    #     # context.update(csrf(request))    # Обязательно добавьте в шаблон защитный токен
    #
    #     return render(request, template_name=self.template_name, context=context)
    #
    # def post(self, request, *args, **kwargs):
    #     context = {}
    #
    #     form = ContactForm(request.POST)
    #
    #     # Если не выполнить проверку на правильность ввода данных,
    #     # то не сможем забрать эти данные из формы... хотя что здесь проверять?
    #     if form.is_valid():
    #         email_subject = 'EVILEG :: Сообщение через контактную форму '
    #         email_body = "С сайта отправлено новое сообщение\n\n" \
    #                      "Имя отправителя: %s \n" \
    #                      "E-mail отправителя: %s \n\n" \
    #                      "Сообщение: \n" \
    #                      "%s " % \
    #                      (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'])
    #
    #         # и отправляем сообщение
    #         # send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['target_email@example.com'], fail_silently=False)
    #
    #     return render(request, template_name=self.template_name, context=context)