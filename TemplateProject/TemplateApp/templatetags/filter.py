from django import template
register = template.Library()

@register.filter(name='secondfilter')
def second(value):
    return value[1]