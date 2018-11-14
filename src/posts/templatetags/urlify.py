"""Converts any text to urlified"""
from urllib.parse import quote_plus

from django import template

register = template.Library()

@register.filter
def urlify(value):
    """return urlified version of value"""
    return quote_plus(value)
    