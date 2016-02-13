from __future__ import unicode_literals

import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from cartridge.shop.models import ProductVariation
from cartridge.shop.templatetags.shop_tags import _order_totals

register = template.Library()


@register.inclusion_tag("shop/includes/order_totals_offcanvas.html", takes_context=True)
def order_totals_offcanvas(context):
    """
    Off-canvas version of order_totals.
    """
    return _order_totals(context)


@register.filter(needs_autoescape=True)
def parse_description(value, autoescape=True):
    """
    Split product description to title and options to allow different styling.
    Returns html with title and options in two lines with different classes:
    'title' and 'options'.
    """
    option_fields = ProductVariation.option_fields()
    if option_fields:
        first_option_label = option_fields[0].verbose_name
        m = re.match(ur"(.*\w*)\s(%s.*)$" % first_option_label, value, re.I | re.U)
    if m:
        title = m.group(1)
        options = m.group(2)
        if autoescape:
            esc = conditional_escape
        else:
            esc = lambda x: x
        return mark_safe(
            "<span class='title'>%s</span><br><span class='options'>%s</span>" % (esc(title), esc(options)))
    else:
        return value
