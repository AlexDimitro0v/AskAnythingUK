from django import template
register = template.Library()

@register.simple_tag
def let(val=None):
  return val
