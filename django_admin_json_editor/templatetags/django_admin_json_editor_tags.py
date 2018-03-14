# Credit to this gist which came up high in google results: https://gist.github.com/jtiai/5002929
from django import template
from django.utils.safestring import mark_safe

import json

register = template.Library()

@register.filter(name='json_dumps')
def json_dumps(data):
    return mark_safe(json.dumps(data))
