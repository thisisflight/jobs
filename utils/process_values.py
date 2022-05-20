from collections import defaultdict

from django.db.models import QuerySet


def get_values_data(data: QuerySet) -> dict:
    """Обрабатывает данные из базы и возвращает словарь
    с заголовками тегов в качестве ключей и списком заголовков
    навыков в качестве значений"""
    values_data = defaultdict(list)
    for value in data:
        values_data[value.tag.title].append(value.title)
    return dict(values_data)
