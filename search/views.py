from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from main.mixins import CategoryDetailMixin
from .documents import ProductDocument
from main.models import Product, Iphone, Ipad, CategoryProduct, LatestProducts


class SearchView(CategoryDetailMixin, DetailView):
    # CT_MODEL_CLASS = {
    #     'iphone': Iphone,
    #     'ipad': Ipad
    # }
    #
    # def dispatch(self, request, *args, **kwargs):
    #     """ Возвращаем выбранную пользователем модель товара """
    #     self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
    #     self.queryset = self.model._base_manager.all()
    #     return super(SearchView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                      {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
        test = []
        if q:
            products = ProductDocument.search().query('match', title=q)
            # for i in products:
            #     print(i.category)
            for i in products:
                test.append(Product.objects.get(id=i['id']))
            print(test)
        else:
            products = ''

        return render(request, 'search/search.html', {'products': products, 'categories': categories, 'test': test})

    template_name = 'search/search.html'
    context_object_name = 'latest_question_list'
    model = Product


#
# class SearchView(View):
#     def get(self, request, *args, **kwargs):
#         customer = request.user
#         categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
#                       {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
#         products = Product.objects.all()
#         test = OrderItem.objects.all()
#         return render(request, 'search/search.html', {'products': products, 'quantity': test, 'categories': categories})
