from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    # path('add/<str:product_id>/', views.cart_add, name='cart_add'),
    path('add/<str:title>/', views.cart_add, name='cart_add'),
    path('cart_create/', views.cart_create, name='cart_create'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),  # можно удалить
    path('update_item/', views.updateItem, name='update_item'),
]