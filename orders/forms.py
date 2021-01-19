from django import forms
from django.forms import TextInput

from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(label='სახელი')
    last_name = forms.CharField(label='გვარი')
    email = forms.CharField(label='email')
    address = forms.CharField(label='მისამართი')
    postal_code = forms.CharField(label='ტელეფონი')
    city = forms.CharField(label='ქალაქი')



    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']