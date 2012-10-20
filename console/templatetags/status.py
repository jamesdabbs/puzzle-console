from django import template
from django.utils.safestring import mark_safe

from console.models import PuzzleProgress as P

register = template.Library()


@register.simple_tag
def status(item):
    cls = {
        P.OPENED: 'info',
        P.SOLVED: 'success',
        P.FAILED: 'warning'
    }.get(item.status)
    text = item.get_status_display()
    return mark_safe('<span class="label label-%s">%s</span>' % (cls, text))


@register.simple_tag
def youtube(url):
    frag = url.split('=')[-1]
    return mark_safe('<div><iframe width="560" height="315" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % frag)
