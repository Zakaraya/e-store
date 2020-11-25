from django.urls import path, include

from . import views
from .views import BaseView, ProductDetailView, CategoryDetailView, LoginView

app_name = 'main'

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('login/', LoginView.as_view(), name='login'),

]
