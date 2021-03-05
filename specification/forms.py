from django import forms

from .models import FeatureValidator, CategoryFeature
from main.models import CategoryProduct


class NewCategoryFeatureKeyForm(forms.ModelForm):

    class Meta:
        model = CategoryFeature
        fields = '__all__'


class NewCategoryForm(forms.ModelForm):

    class Meta:
        model = CategoryProduct
        fields = '__all__'


class FeatureValidatorForm(forms.ModelForm):

    class Meta:
        model = FeatureValidator
        fields = ['category']
