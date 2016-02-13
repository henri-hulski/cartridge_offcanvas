from __future__ import unicode_literals

from django.conf.urls import url

from mezzanine.conf import settings

from offcanvas_cart import views


_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^add_product%s$" % _slash, views.add_product, name="add_product"),
    url("^update_cart%s$" % _slash, views.update_cart, name="update_cart"),
    url("^refresh_cart_icon%s$" % _slash, views.refresh_cart_icon, name="refresh_cart_icon"),
]
