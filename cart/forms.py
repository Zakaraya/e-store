from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20)]  # не больше 20 товара в корзине


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, required=False, initial=False, label='Количество')
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, required=False, initial=False, label='რაოდენობა')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
