from __future__ import unicode_literals
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms.formsets import DELETION_FIELD_NAME
from cartridge.shop.forms import CartItemForm
from cartridge.shop.models import Cart, CartItem


class OffCartItemForm(CartItemForm):
    """
    Model form for each item in the off canvas cart - used for the
    ``OffCartItemFormSet`` below which controls editing the entire cart.
    """

    class Meta:
        model = CartItem
        fields = ('quantity',)
        widgets = {
            'quantity': forms.HiddenInput,
        }


class HiddenDeleteInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(HiddenDeleteInlineFormSet, self).add_fields(form, index)
        form.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput()


OffCartItemFormSet = inlineformset_factory(Cart, CartItem, form=OffCartItemForm,
                                           formset=HiddenDeleteInlineFormSet, extra=0)
