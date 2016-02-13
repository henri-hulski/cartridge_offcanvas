from __future__ import unicode_literals

import re

from django.contrib.messages import info
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from mezzanine.conf import settings
from cartridge.shop.forms import AddProductForm
from cartridge.shop.models import Product
from cartridge.shop.utils import recalculate_cart

from offcanvas_cart.forms import OffCartItemFormSet


@never_cache
def add_product(request, form_class=AddProductForm):
    """
    Display a product - handling adding the product the off canvas cart.
    """

    m = re.search(r"/product/(.*)/$", request.POST.get("slug"))
    slug = m.group(1)
    published_products = Product.objects.published(for_user=request.user)
    product = get_object_or_404(published_products, slug=slug)
    if request.is_ajax() and request.POST:
        to_cart = request.POST.get("add_cart")
        add_product_form = form_class(request.POST or None, product=product, to_cart=to_cart)
        if to_cart:
            if add_product_form.is_valid():
                quantity = add_product_form.cleaned_data["quantity"]
                request.cart.add_item(add_product_form.variation, quantity)
                info(request, _("Item added to cart"))
                recalculate_cart(request)
                return update_cart(request)
            else:
                error = add_product_form.non_field_errors()[0]
                return JsonResponse({'error': error})

    else:
        raise Http404


@never_cache
def update_cart(request, template="shop/includes/offcanvas_cart.html", cart_formset_class=OffCartItemFormSet):
    """
    Display cart and handle removing items from the cart.
    """
    cart_formset = cart_formset_class(instance=request.cart)

    if request.is_ajax():
        if request.POST and request.POST.get("update_cart"):
            valid = request.cart.has_items()
            if not valid:
                # Session timed out.
                info(request, _("Your cart has expired"))
            else:
                cart_formset = cart_formset_class(request.POST, instance=request.cart)
                valid = cart_formset.is_valid()
                if valid:
                    cart_formset.save()
                    info(request, _("Cart updated"))
                    recalculate_cart(request)
                    cart_formset = cart_formset_class(instance=request.cart)
                else:
                    # Reset the cart formset so that the cart
                    # always indicates the correct quantities.
                    # The user is shown their invalid quantity
                    # via the error message, which we need to
                    # copy over to the new formset here.
                    errors = cart_formset._errors
                    cart_formset = cart_formset_class(instance=request.cart)
                    cart_formset._errors = errors
        elif request.POST and request.POST.get("add_cart"):
            cart_formset = cart_formset_class(instance=request.cart)

        context = {"off_cart_formset": cart_formset}
        settings.clear_cache()
        return TemplateResponse(request, template, context)

    else:
        raise Http404


@never_cache
def refresh_cart_icon(request, template="shop/includes/open_cart_button.html"):
    """
    Update number in cart-icon after updating cart.
    """

    if request.is_ajax():
        return TemplateResponse(request, template)
    else:
        raise Http404
