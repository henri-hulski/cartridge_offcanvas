function removeItem(e) {
    var item = $(e).parents('.item'),
        del = item.find('input:hidden[id $= "-DELETE"]'),
        removeButton = item.find('#remove-wrapper');
    del.val('on');
    updateCart(removeButton);
}

function incrementItem(e) {
    var item = $(e).parents('.item'),
        qtyField = item.find('input:hidden[id $= "-quantity"]'),
        qty = parseInt(qtyField.val()) + 1,
        numberField = item.find('.number');
    qtyField.val(qty);
    updateCart(numberField);
}

function decrementItem(e) {
    var item = $(e).parents('.item'),
        qtyField = item.find('input:hidden[id $= "-quantity"]'),
        qty = parseInt(qtyField.val()) - 1,
        numberField = item.find('.number');
    qtyField.val(qty);
    updateCart(numberField);
}

function addProduct() {
    var form = $('#add-cart'),
        openCartField = form.find('.open-cart').first(),
        slug = window.location.pathname;
    openCartField.val('on');
    $.ajax({
        type: "POST",
        url: "/shop/api/add_product/",
        data: form.serialize() + "&slug=" + slug,
        beforeSend: function() {
            $('#add-product-spinner').show("slow");
        },
        success: function(data) {
            if (data['error']) {
                var html = "<div class='alert alert-danger non-field-error'>" + data['error'] + "</div>";
                $('#add-product-errors').html(html);
            } else {
                $('#off-cart').html(data);
                refreshCartIcon();
                openCartField.trigger('click');
                var itemsDiv = $("#off-cart-line-items");
                itemsDiv.animate({ scrollTop: itemsDiv.prop("scrollHeight")}, 2400);
            }
        },
        complete: function() {
            $('#add-product-spinner').hide("slow");
        }
    });
}

function updateCart(spinnerContainer) {
    var form = $("#off-cart-form");
    $.ajax({
        type: "POST",
        url: "/shop/api/update_cart/",
        dataType: "html",
        data: form.serialize(),
        beforeSend: function() {
            if (spinnerContainer) {
                spinnerContainer.html('<img src="/static/img/spinner.gif" alt="Loading..." />');
            }
        },
        success: function(data) {
            var scrollPos = $("#off-cart-line-items").scrollTop();
            $('#off-cart').html(data);
            $("#off-cart-line-items").scrollTop(scrollPos);
            refreshCartIcon();
			if (checkoutActive) {
			    cartChanged = true;
			}
        }
    });
}

function refreshCartIcon() {
    $.ajax({
        type: "GET",
        url: "/shop/api/refresh_cart_icon/",
        dataType: "html",
        success: function(data) {
            $('#open-cart').html(data);
        }
    });
}
