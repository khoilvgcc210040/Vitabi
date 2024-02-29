# custom_filters.py
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def time_to_string(value):
    return value.strftime('%H:%M:%S')

@register.filter
def to_float(value):
    try:
        return float(value.replace('%', ''))
    except ValueError:
        return 0

