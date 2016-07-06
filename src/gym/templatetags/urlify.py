from django.utils.six.moves.urllib.parse import (
    quote, quote_plus, unquote, unquote_plus, urlencode as original_urlencode,
    urlparse,
)
from django import template

register = template.Library()
@register.filter
def urlify(value):
	return quote_plus(value)


