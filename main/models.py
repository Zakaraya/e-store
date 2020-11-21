from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def get_models_for_count(*model_names):
    """Функция получения количества товаров в определенной категории"""
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, view_name):
    """Функция для получения необходимого view_name для отображения нужного товара obj"""
    ct_model = obj.__class__._meta.model_name
    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductManager:
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        """Функция для вывода всех товаров в обратном порядке на главную страницу"""
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.filter(available=True).order_by('-id')
            # model_products = ct_model.model_class()._base_manager.filter(available=True)
            products.extend(model_products)
        return products


class LatestProducts:
    objects = LatestProductManager()


class CategoryManager(models.Manager):
    """Класс категорий товаров"""

    def get_queryset(self):
        """Получение результата работы queryset'а"""
        return super(CategoryManager, self).get_queryset()

    CATEGORY_NAME_COUNT_NAME = {
        'Айфоны': 'iphone__count',
        'Айпады': 'ipad__count'
    }

    def get_categories_for_left_sidebar(self):
        """Функция получения категорий в sidebar"""
        # # category_models = get_models_for_count('ipad', 'iphone')
        # category_models = get_models_for_count('ipad', 'iphone')
        # queryset_categories = list(self.get_queryset().annotate(*category_models))
        # # return [
        # #     dict(name=item['category_name'], slug=item['slug'],
        # #          count=item[self.CATEGORY_NAME_COUNT_NAME[item['category_name']]])
        # #     for item in queryset_categories]
        # data = [
        #     dict(name=item.category_name, url=item.get_absolute_url(), count=getattr(item, self.CATEGORY_NAME_COUNT_NAME[item.category_name]))
        #     for item in queryset_categories
        # ]
        # return data
        # pass


class CategoryProduct(models.Model):
    """"Таблица категорий продуктов"""
    category_name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('main:category_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Таблица товаров"""

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    category = models.ForeignKey(CategoryProduct, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование продукта')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение продукта')
    description = models.TextField(verbose_name='Описание продукта', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена продукта')
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество товара на складе')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Iphone(Product):
    """Таблица с Iphones"""
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    memory = models.CharField(max_length=255, verbose_name='Память')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Основная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')
    face_id = models.BooleanField(default=True, verbose_name='Наличие FaceID')
    face_id_technology = models.CharField(max_length=255, null=True, blank=True, verbose_name='Технология FaceID')

    def __str__(self):
        return '{} : {}'.format(self.category.category_name, self.title)

    def get_absolute_url(self):
        """Функция получения названия view, которая передается в get_product_url для отображения необходимого товара"""
        return get_product_url(self, 'main:product_detail')
    #
    # class Meta:
    #     ordering = ('title',)
    #     index_together = (('id', 'slug'),)


class Ipad(Product):
    """Таблица с Ipads"""
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    memory = models.CharField(max_length=255, verbose_name='Память')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Основная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return '{} : {}'.format(self.category.category_name, self.title)

    def get_absolute_url(self):
        """Функция получения названия view, которая передается в get_product_url для отображения необходимого товара"""
        return get_product_url(self, 'main:product_detail')  # product_detail берется из urls.py


# class CartProduct(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#
# class Cart(models.Model):
#     products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')