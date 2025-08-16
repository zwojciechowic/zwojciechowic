from django import template

register = template.Library()

@register.filter
def pluralize_pl(value):
    value = int(value)
    if value == 1:
        return ''
    if 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return 'y'
    return 'ów'