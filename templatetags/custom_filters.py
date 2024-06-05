from django import template

register = template.Library()


@register.filter
def skip(iterable, index):
    """
    Custom template filter to skip rendering the current iteration of a loop.
    """
    return iterable[:index] + iterable[index + 1:]
