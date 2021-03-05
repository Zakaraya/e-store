from django.contrib import admin
from django.forms import ModelChoiceField

from .models import *


# class ProductIphoneAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'category':
#             return ModelChoiceField(CategoryProduct.objects.filter(slug='iphones'))
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#
# class ProductIpadAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'category':
#             return ModelChoiceField(CategoryProduct.objects.filter(slug='ipads'))
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
class ProductAdmin(admin.ModelAdmin):
    pass
    #change_form_template = 'custom_admin/change_form.html'
    # exclude = ('features',)


admin.site.register(CategoryProduct)
# admin.site.register(Ipad, ProductIpadAdmin)
# admin.site.register(Iphone, ProductIphoneAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
