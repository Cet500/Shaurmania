from Shaurmania.settings import DEBUG, COMPRESS_ENABLED, IS_HALLOWEEN, IS_NEW_YEAR


def feature_flags(request):
	return {
		'DEBUG'            : DEBUG,
		'COMPRESS_ENABLED' : COMPRESS_ENABLED,
		'IS_HALLOWEEN'     : IS_HALLOWEEN,
		'IS_NEW_YEAR'      : IS_NEW_YEAR
	}


def cart_meta(request):
	from cart.models import Cart

	if request.user.is_authenticated:
		rows = Cart.objects.filter(user=request.user).values_list('quanity', flat=True)
	else:
		if not request.session.session_key:
			request.session.save()
		rows = Cart.objects.filter(session_key=request.session.session_key).values_list('quanity', flat=True)

	return {
		'cart_count': sum(rows)
	}
