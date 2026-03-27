import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from cart.models import Cart, Order, Promocode
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


def _get_cart_pricing(request, promo_code=None):
    entries = _get_cart_queryset(request)
    lines = []
    subtotal = 0
    total_count = 0
    promo = None
    discount_percent = 0

    if promo_code:
        now = timezone.now().date()
        promo = Promocode.objects.filter(
            code_name__iexact=promo_code.strip(),
            date_add__lte=now,
            date_end__gte=now,
        ).first()
        if promo:
            discount_percent = max(0, min(int(promo.discount), 100))

    for entry in entries:
        sh = entry.item
        q = entry.quanity
        line_subtotal = sh.price * q
        line_discount = round(line_subtotal * (discount_percent / 100))
        line_total = line_subtotal - line_discount
        lines.append({
            'entry': entry,
            'shaurma': sh,
            'quantity': q,
            'unit_price': sh.price,
            'line_subtotal': line_subtotal,
            'line_discount': line_discount,
            'line_total': line_total,
        })
        subtotal += line_subtotal
        total_count += q

    order_discount = round(subtotal * (discount_percent / 100))
    total = subtotal - order_discount

    return {
        'lines': lines,
        'subtotal': subtotal,
        'discount': order_discount,
        'discount_percent': discount_percent,
        'total': total,
        'count': total_count,
        'promo': promo,
        'promo_code': promo_code or '',
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


def checkout(request):
    promo_code = request.POST.get('promo_code', '').strip() if request.method == 'POST' else request.GET.get('promo', '').strip()
    pricing = _get_cart_pricing(request, promo_code=promo_code)
    empty_cart = len(pricing['lines']) == 0

    if request.method == 'POST' and request.POST.get('action') == 'confirm':
        if empty_cart:
            return redirect('cart')

        order_code = timezone.now().strftime('ORD-%Y%m%d-') + uuid.uuid4().hex[:6].upper()
        session_key = _get_or_create_session_key(request)

        for row in pricing['lines']:
            Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=session_key,
                shaurma=row['shaurma'],
                quantity=row['quantity'],
                unit_price=row['unit_price'],
                line_subtotal=row['line_subtotal'],
                line_discount=row['line_discount'],
                line_total=row['line_total'],
                order_code=order_code,
                promocode=pricing['promo'],
                order_subtotal=pricing['subtotal'],
                order_discount=pricing['discount'],
                order_total=pricing['total'],
                payer_name='Galactical Bank Inc.',
                is_demo_payment=True,
            )

        _get_cart_queryset(request).delete()

        request.session['last_paid_order'] = {
            'order_code': order_code,
            'total': pricing['total'],
            'count': pricing['count'],
        }
        return redirect('checkout_thanks')

    promo_error = ''
    if promo_code and not pricing['promo']:
        promo_error = 'Промокод не найден или просрочен.'

    ctx = {
        'pricing': pricing,
        'promo_error': promo_error,
        'bank_name': 'Galactical Bank Inc.',
    }
    return render(request, 'cart/checkout.jinja', context=ctx)


def checkout_thanks(request):
    order_data = request.session.get('last_paid_order')
    if not order_data:
        return redirect('cart')
    return render(request, 'cart/thanks.jinja', context={'order': order_data})
