from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('process_order/', views.processOrder, name="process_order"),
    path('admin/order/<order_id>', views.admin_order_detail, name='admin_order_detail'),
    # path('process_payment/', views.process_payment, name='process_payment'),
]