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
        if isinstance(self.get_object(), CategoryProduct):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = CategoryProduct.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.all()
            # context['cart_product_form'] = CartAddProductForm()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryProduct.objects.get_categories_for_left_sidebar()
        return context

