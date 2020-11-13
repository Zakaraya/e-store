from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import *
from .mixins import CategoryDetailMixin


class BaseView(View):
    """Базовое представление"""

    def get(self, request, *args, **kwargs):
        categories = CategoryProduct.objects.get_categories_for_left_sidebar()
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
