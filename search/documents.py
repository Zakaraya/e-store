# from django_elasticsearch_dsl import Document, Index, NestedField, fields, TextField
# from django_elasticsearch_dsl.registries import registry
# from main.models import Product, CategoryProduct, get_product_url
# from django.urls import reverse
#
#
# @registry.register_document
# class ProductDocument(Document):
#     category = fields.ObjectField(properties={
#         'category_name': fields.TextField(),
#         'slug': fields.TextField(),
#     })
#
#     # category = NestedField(properties={
#     #     'value': fields.FloatField(),
#     #     'id': fields.IndegerField()
#     # })
#     class Index:
#         # Name of the Elasticsearch index
#         name = 'product'
#         # See Elasticsearch Indices API reference for available settings
#         settings = {'number_of_shards': 1,
#                     'number_of_replicas': 0}
#
#     class Django:
#         model = Product  # The model associated with this Document
#
#         # The fields of the model you want to be indexed in Elasticsearch
#         fields = [
#             'title',
#             'id',
#             'slug',
#             'image',
#             'description',
#             'price',
#         ]
#         related_models = [CategoryProduct]
#
#     def get_queryset(self):
#         """Not mandatory but to improve performance we can select related in one sql request"""
#         return super(ProductDocument, self).get_queryset().select_related(
#             'category'
#         )
#
#     def get_instances_from_related(self, related_instance):
#         """If related_models is set, define how to retrieve the Car instance(s) from the related model.
#         The related_models option should be used with caution because it can lead in the index
#         to the updating of a lot of items.
#         """
#         if isinstance(related_instance, CategoryProduct):
#             return related_instance.product_set.all()
#
#     # def get_absolute_url(self):
#     #     """Функция получения названия view, которая передается в get_product_url для отображения необходимого товара"""
#     #     # return get_product_url(self, 'search:search')
#     #     return get_product_url(self, 'main:product_detail')
#     def get_absolute_url(self):
#         # !!! КОСТЫЛЬ !!! ИСПРАВИТЬ !!!
#         print(self.category['slug'][:-1])
#         return reverse('main:product_detail', kwargs={'ct_model': self.category['slug'][:-1], 'slug': self.slug})
