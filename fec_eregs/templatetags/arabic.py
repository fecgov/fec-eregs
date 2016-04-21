from django import template
from roman import fromRoman
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='arabic')
@stringfilter
def arabic(value):
    #capitalizes roman numerals and converts to arabic.
    return fromRoman(value.upper())