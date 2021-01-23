from django import template
from django.utils.safestring import mark_safe

import re

register = template.Library()

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

@register.filter("add_css_class")
def add_css_class(obj, css_class):
    match = re.search('class=".*"', obj)
    match = match.group(0)
    current_class = match[0:findnth(match, '"', 1)]
    new_class = match[0:findnth(match, '"', 1)] + " " + css_class
    

    return mark_safe(obj.replace(current_class, new_class))
