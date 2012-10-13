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
