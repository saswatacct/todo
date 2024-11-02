from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def ic(name: str, classes: str = "") -> str:
    """Return a Bootstrap icon tag

    Args:
        name (str): Icon name
        classes (str, optional): Additional classes. Defaults to ''.

    Returns:
        str: Icon tag
    """

    return mark_safe(f'<i class="bi bi-{name} {classes}"></i>')
