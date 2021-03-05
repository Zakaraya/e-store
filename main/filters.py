

from .models import Product
import django_filters


class ProductFilter(django_filters.FilterSet):
    # diagonal = django_filters.BooleanFilter(name='diagonal', widget=forms.CheckboxInput)
    # diagonal = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    # price__range = django_filters.NumericRangeFilter
    price =django_filters.RangeFilter(label='People range')
    class Meta:
        model = Product
        fields = {
            'title': ['icontains'],
            # 'price': ['gt', 'lt'],
            # 'diagonal': ['diagonal'],
        }
