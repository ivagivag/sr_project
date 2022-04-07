from django import template

register = template.Library()


@register.simple_tag
def percentage(value):
    fb, total = [int(x) for x in value.split('/')]
    result = fb / total * 100
    return int(result)
