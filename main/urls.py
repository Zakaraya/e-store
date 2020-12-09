from django.urls import path
from .views import BaseView, ProductDetailView, CategoryDetailView, LoginView, RegistrationView, ProfileView, EContactsView,contact
from django.contrib.auth.views import LogoutView

app_name = 'main'

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('contacts/', EContactsView.as_view(), name='contacts'),
    path('contact/', contact, name='contact'),

]
