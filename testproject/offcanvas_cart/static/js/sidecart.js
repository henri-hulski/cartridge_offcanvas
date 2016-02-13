(function() {

	var isOpenCart = false,
		bodyEl = $(document.body);

	function initEvents() {
		var wrapper = $('#open-cart').parent(),
			openCart = $('.open-cart'),
            closeCart = document.getElementById('close-cart');

		wrapper.on('click', '#open-cart', toggleCart);
		openCart.on('click', toggleCart);
		if (closeCart) {
			closeCart.addEventListener('click', toggleCart);
		}

		// Close the cart if the target it´s not the cart or one of its descendants.
		document.querySelector('.content-wrap').addEventListener('click', function(e) {
			var target = e.target,
				opencart = document.getElementById('open-cart'),
				opencartImg = opencart.getElementsByTagName('img')[0];
			if (isOpenCart && target !== opencart && target !== opencartImg && target !== openCart[0]) {
				toggleCart();
			}
		});
	}

	function toggleCart() {
		if (isOpenCart) {
			bodyEl.removeClass('show-cart');
			if (checkoutActive && cartChanged) {
			    window.location = window.location.href.split("#")[0];
			}
		} else {
			bodyEl.addClass('show-cart');
		}
		isOpenCart = !isOpenCart;
	}

	initEvents();

})();
