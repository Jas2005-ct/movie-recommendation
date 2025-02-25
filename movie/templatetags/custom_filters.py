from django import template

register = template.Library()

@register.filter
def times(value, char):
    return char * value
