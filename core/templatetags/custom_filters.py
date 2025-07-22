from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    print ("getting " + attr + " from ")
    print (obj)
    return getattr(obj, attr, None)