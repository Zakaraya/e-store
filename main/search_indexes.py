# from haystack import indexes
# from .models import Product
# from django_elasticsearch_dsl import (
#     Document,
#     Date,
#     Keyword,
#     Text,
#     Boolean,
#     Integer
# )

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Product


# class PostIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     created = indexes.DateTimeField(model_attr='created')
#
#     def get_model(self):
#         return Product
#
#     # def index_queryset(self, using=None):
#     #     return self.get_model().created.all()
# class BlogIndex(Document):
#
#     pk = Integer()
#     title = Text(fields={'raw': Keyword()})
#     created_at = Date()
#     body = Text()
#     tags = Keyword(multi=True)
#     is_published = Boolean()
#
#     class Meta:
#         index = 'blog'

@registry.register_document
class CarDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'products'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'slug',
            'description',
            'type',
        ]