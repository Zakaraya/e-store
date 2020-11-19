from django.urls import path, include

from .views import BaseView, ProductDetailView, CategoryDetailView

# app_name = 'main'

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail')
]
