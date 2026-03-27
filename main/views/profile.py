from django.shortcuts import render, redirect, get_object_or_404
from main.models import User
from cart.models import Order


def user(request, username):
	profile_user = get_object_or_404(User, username=username)
	is_owner = request.user.is_authenticated and request.user.username == username

	if not is_owner and not profile_user.is_open:
		return redirect('user_closed')

	order_history = []
	if is_owner:
		rows = Order.objects.filter(user=profile_user).select_related('shaurma', 'promocode').order_by('-date')
		order_map = {}
		for row in rows:
			if row.order_code not in order_map:
				order_map[row.order_code] = {
					'order_code': row.order_code,
					'date': row.date,
					'subtotal': row.order_subtotal,
					'discount': row.order_discount,
					'total': row.order_total,
					'promocode': row.promocode.code_name if row.promocode else None,
					'order_lines': [],
				}
			order_map[row.order_code]['order_lines'].append(row)
		order_history = list(order_map.values())

	return render( request, 'main/user.jinja', {
		'profile_user': profile_user,
		'is_owner': is_owner,
		'order_history': order_history,
	} )


def user_closed(request):
	return render( request, 'main/_parts/user_closed.jinja' )
