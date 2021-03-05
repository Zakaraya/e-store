from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, View

from cart.forms import CartAddProductForm
from specification.models import ProductFeatures
from .models import *
from .mixins import CategoryDetailMixin
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from orders.models import Order, OrderItem

from django.views import View
from django.core.mail import send_mail

from main.filters import ProductFilter


class BaseView(View):
    """Базовое представление"""

    def get(self, request, *args, **kwargs):
        # categories = CategoryProduct.objects.get_categories_for_left_sidebar()
        # ИСПРАВИТЬ!!!!!!!!!!!!!
        # categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
        #               {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
        categories = CategoryProduct.objects.all()
        # products = LatestProducts.objects.get_products_for_main_page('iphone', 'ipad')
        products = Product.objects.all()

        filter = ProductFilter(request.GET, queryset=products)

        context = {
            'categories': categories,
            'products': products,
            'filter': filter,
        }
        return render(request, 'main/base.html', context)


# class ProductDetailView(CategoryDetailMixin, DetailView):
#     """Класс для отобраения порбродной информации для выбранного товара"""
#     model = Product
#     context_object_name = 'product'
#     template_name = 'main/product_detail.html'
#     slug_url_kwarg = 'slug'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['categories'] = self.get_object().category.__class__.objects.all()
#         return context

class ProductDetailView(DetailView):
    """Класс для отобраения порбродной информации для выбранного товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['categories'] = self.get_object().category.__class__.objects.all()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     cart_product_form = CartAddProductForm()
    #     categories = CategoryProduct.objects.all()
    #     context['cart_product_form'] = cart_product_form
    #     context['categories'] = categories
    #     return context


class CategoryDetailView(DetailView):
    """Класс для оторбажения товаров, относящихся к определенной категории"""

    model = CategoryProduct
    queryset = CategoryProduct.objects.all()
    context_object_name = 'category'
    template_name = 'main/category_detail.html'
    slug_url_kwarg = 'slug'

    # def get(self, request, slug, **kwargs):
    #     category_products = Product.objects.filter(category__slug=slug)
    #     categories = CategoryProduct.objects.all()
    #
    #     return render(request, 'main/category_detail.html',
    #                   {'category_products': category_products, 'slug': slug, 'categories': categories})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        category = self.get_object()
        context['categories'] = self.model.objects.all()
        if not query and not self.request.GET:
            context['category_products'] = category.product_set.all()
            return context
        if query:
            products = category.product_set.filter(Q(title__icontains=query))
            context['category_products'] = products
            return context
        url_kwargs = {}
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)
        q_condition_queries = Q()
        for key, value in url_kwargs.items():
            if value == '':
                continue
            elif isinstance(value, list):
                q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
            elif key == 'product__price__gt':
                q_condition_queries.add(Q(**{'product__price__gt': value}), Q.AND)
            elif key == 'product__price__lt':
                q_condition_queries.add(Q(**{'product__price__lt': value}), Q.AND)
            else:
                q_condition_queries.add(Q(**{'value': value}), Q.OR)
        pf = ProductFeatures.objects.filter(
            q_condition_queries
        ).prefetch_related('product', 'feature').values('product_id')

        products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
        context['category_products'] = products
        return context


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
        categories = CategoryProduct.objects.all()
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


def product_list_sorting(request, pk):
    categories = CategoryProduct.objects.all()
    if pk == 1:
        filter = Product.objects.all()
    elif pk == 2:
        filter = Product.objects.filter(available=True).order_by('price')
    else:
        filter = Product.objects.filter(available=True).order_by('-price')
    return render(request, 'main/sorting.html', {'products': filter, 'categories': categories})


def product_list_filter(request):
    product = Product.objects.all()
    categories = CategoryProduct.objects.all()
    filter = ProductFilter(request.GET, queryset=product)
    return render(request, 'main/filters.html', {'filter': filter, 'categories': categories})
