from django import template

register = template.Library()

@register.filter(name='plural_suffix_pl')
def plural_suffix_pl(value):
    value = int(value)
    if value == 1:
        return ''
    if 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return 'y'  # 2,3,4,22,23,24,32,33,34 itd.
    return 'ów'  # 0,5,6,7,8,9,10-21,25-31 itd.