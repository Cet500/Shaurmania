from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from main.models import Shaurma


def _get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def _get_cart_queryset(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('item')
    session_key = _get_or_create_session_key(request)
    return Cart.objects.filter(session_key=session_key).select_related('item')


def _serialize_cart(request):
    entries = _get_cart_queryset(request)
    items = []
    total = 0
    total_count = 0
    for entry in entries:
        sh = entry.item
        q = entry.quanity
        item_total = sh.price * q
        items.append({
            'id': sh.id,
            'name': sh.name,
            'slug': sh.slug,
            'price': sh.price,
            'quantity': q,
            'total': item_total,
            'picture': sh.picture.url if getattr(sh, 'picture', None) else None,
        })
        total += item_total
        total_count += q
    return {
        'items': items,
        'total': total,
        'count': total_count,
    }


def cart(request):
    data = _serialize_cart(request)
    ctx = {
        'cart': [
            {
                'shaurma': get_object_or_404(Shaurma, id=item['id']),
                'quantity': item['quantity'],
                'total': item['total'],
            }
            for item in data['items']
        ],
        'cart_total': data['total'],
        'cart_count': data['count'],
    }
    return render( request, 'cart/cart.jinja', context=ctx )


def cart_add(request, shaurma_id):
    sh = get_object_or_404(Shaurma, id=shaurma_id)
    if request.user.is_authenticated:
        entry, created = Cart.objects.get_or_create(user=request.user, item=sh, defaults={'quanity': 1})
        if not created:
            entry.quanity = entry.quanity + 1
            entry.save(update_fields=['quanity'])
    else:
        session_key = _get_or_create_session_key(request)
        entry, created = Cart.objects.get_or_create(session_key=session_key, item=sh, defaults={'quanity': 1})
        if not created:
            entry.quanity = entry.quanity + 1
            entry.save(update_fields=['quanity'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(_serialize_cart(request))

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
        session_key = _get_or_create_session_key(request)
        try:
            entry = Cart.objects.get(session_key=session_key, item=sh)
            if entry.quanity > 1:
                entry.quanity -= 1
                entry.save(update_fields=['quanity'])
            else:
                entry.delete()
        except Cart.DoesNotExist:
            pass

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(_serialize_cart(request))

    return redirect('cart')
