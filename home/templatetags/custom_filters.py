# custom_filters.py
from django import template
from datetime import datetime
import re

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
    
@register.filter(name='hospital_id')
def hospital_id(value, arg):
    return value.get(arg)

@register.filter(name='get_distance_info')
def get_distance_info(distance_infos, hospital_id):
    return distance_infos.get(str(hospital_id), {'distance_text': 'Unknown', 'duration_text': 'Unknown'})

