from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    print ("getting " + attr + " from ")
    print (obj)
    return getattr(obj, attr, None)

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except:
        return ''