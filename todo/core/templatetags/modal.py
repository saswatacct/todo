from django.template import Library
from django.urls import reverse
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def modalurl(name: str, **kwargs) -> str:
    """Create modal request attributes.

    Args:
        name (str): Url reverse name

    Returns:
        str: Attributes string marked as safe HTML
    """
    url = reverse(name, kwargs=kwargs)

    return mark_safe(f'hx-get="{url}" hx-target=".modal"')
