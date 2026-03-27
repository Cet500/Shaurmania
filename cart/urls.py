from django.urls import path
from . import views


urlpatterns = [

	# CART =================================================
	path( '',                         views.cart, name = 'cart' ),
	path( 'add/<int:shaurma_id>',    views.cart_add, name = 'cart_add' ),
	path( 'remove/<int:shaurma_id>', views.cart_remove, name = 'cart_remove' ),
	path( 'checkout',                views.checkout, name = 'checkout' ),
	path( 'checkout/thanks',         views.checkout_thanks, name = 'checkout_thanks' ),

]
