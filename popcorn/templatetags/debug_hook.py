from django import template

register = template.Library()

@register.filter
def debug_hook(obj):
    print(obj)
    return ""
