from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from cart.forms import CartAddProductForm
from .models import *


class CategoryDetailMixin(SingleObjectMixin):
    """Возможность добавления категорий на все страницы"""
    CATEGORY_SLUG2PRODUCT_MODEL = {
        'iphones': Iphone,
        'ipads': Ipad
    }

    def get_context_data(self, **kwargs):
        cart_product_form = CartAddProductForm()
        if isinstance(self.get_object(), CategoryProduct):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = [{'name': 'Айпады', 'url': '/category/ipads/', 'count': 2},
                                     {'name': 'Айфоны', 'url': '/category/iphones/', 'count': 2}]
            context['category_products'] = model.objects.all()

            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryProduct.objects.get_categories_for_left_sidebar()
        context['cart_product_form'] = cart_product_form
        return context
