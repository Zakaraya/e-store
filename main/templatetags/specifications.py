from django import template
from django.utils.safestring import mark_safe

from main.models import Iphone, Ipad

register = template.Library()

TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'iphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Память': 'memory',
        'Разрешение экрана': 'resolution',
        'Объем батареи': 'accum_volume',
        'Основная камера': 'main_cam_mp',
        'Фронтальная камера': 'frontal_cam_mp',
        'Наличие FaceID': 'face_id',
        'Технология FaceID': 'face_id_technology',
    },
    'ipad': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Память': 'memory',
        'Разрешение экрана': 'resolution',
        'Объем батареи': 'accum_volume',
        'Основная камера': 'main_cam_mp',
        'Фронтальная камера': 'frontal_cam_mp',
    },
}


def get_product_specifications(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter()
def product_specifications(product):
    """Функция для вы"""
    model_name = product.__class__._meta.model_name
    if isinstance(product, Iphone):
        if not product.face_id:
            PRODUCT_SPEC['iphone'].pop('Технология FaceID', None)
        else:
            PRODUCT_SPEC['iphone']['Технология FaceID'] = 'face_id_technology'
    return mark_safe(TABLE_HEAD + get_product_specifications(product, model_name) + TABLE_TAIL)
