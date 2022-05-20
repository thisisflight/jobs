from django import template

register = template.Library()


@register.simple_tag
def processing_list_to_string(data, key):
    """Представит в удобочитаемом виде список"""
    return ', '.join(data.get(key, ''))


@register.filter
def processing_dict(data: dict, key: str) -> dict:
    """Вернет ключ словаря"""
    return data.get(key)
