from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from main.models import Shaurma


def cart(request):
    if request.user.is_authenticated:
        # берём корзину из БД
        cart_qs = Cart.objects.filter(user=request.user)
        cart_items = []
        cart_total = 0
        for entry in cart_qs.select_related('item'):
            sh = entry.item
            q = entry.quanity
            item_total = sh.price * q
            cart_items.append({'shaurma': sh, 'quantity': q, 'total': item_total})
            cart_total += item_total
    else:
        # fallback — session (как было)
        cart_data = request.session.get('cart_items', {})
        if isinstance(cart_data, list):
            cart_data = {str(i): 1 for i in cart_data}
            request.session['cart_items'] = cart_data
        cart_items = []
        cart_total = 0
        for id_str, qty in cart_data.items():
            try:
                sh = get_object_or_404(Shaurma, id=int(id_str))
                q = int(qty)
                item_total = sh.price * q
                cart_items.append({'shaurma': sh, 'quantity': q, 'total': item_total})
                cart_total += item_total
            except (ValueError, TypeError):
                continue

    ctx = {'cart': cart_items, 'cart_total': cart_total}
    return render( request, 'cart/cart.jinja', context=ctx )


def cart_add(request, shaurma_id):
    sh = get_object_or_404(Shaurma, id=shaurma_id)
    if request.user.is_authenticated:
        entry, created = Cart.objects.get_or_create(user=request.user, item=sh, defaults={'quanity': 1})
        if not created:
            entry.quanity = entry.quanity + 1
            entry.save(update_fields=['quanity'])
    else:
        cart_data = request.session.get('cart_items', {})
        if isinstance(cart_data, list):
            cart_data = {str(i): 1 for i in cart_data}
        key = str(shaurma_id)
        cart_data[key] = int(cart_data.get(key, 0)) + 1
        request.session['cart_items'] = cart_data
        request.session.modified = True
    return redirect('cart')


def cart_remove(request, shaurma_id):
    sh = get_object_or_404(Shaurma, id=shaurma_id)
    if request.user.is_authenticated:
        try:
            entry = Cart.objects.get(user=request.user, item=sh)
            if entry.quanity > 1:
                entry.quanity -= 1
                entry.save(update_fields=['quanity'])
            else:
                entry.delete()
        except Cart.DoesNotExist:
            pass
    else:
        cart_data = request.session.get('cart_items', {})
        if isinstance(cart_data, list):
            cart_data = {str(i): 1 for i in cart_data}
        key = str(shaurma_id)
        if key in cart_data:
            new_qty = int(cart_data.get(key, 0)) - 1
            if new_qty > 0:
                cart_data[key] = new_qty
            else:
                del cart_data[key]
            request.session['cart_items'] = cart_data
            request.session.modified = True
    return redirect('cart')
