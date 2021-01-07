from django.urls import path
from .views import *
from main.views import ProductDetailView
from django.contrib.auth.views import LogoutView

app_name = 'search'

urlpatterns = [
    # path('', views.search, name='search'),
    path('', SearchView.as_view(), name='search'),

]
