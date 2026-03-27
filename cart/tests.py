from django.test import TestCase
from django.urls import reverse

from cart.models import Cart, Order, Promocode
from main.factories import ShaurmaFactory, UserFactory
from django.utils import timezone


class CartAjaxTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.item = ShaurmaFactory(price=100)

    def test_add_to_cart_ajax_creates_entry_and_returns_json(self):
        url = reverse('cart_add', kwargs={'shaurma_id': self.item.id})
        resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['total'], 100)

        cart_rows = Cart.objects.filter(item=self.item)
        self.assertEqual(cart_rows.count(), 1)

    def test_remove_from_cart_ajax_updates_json_and_deletes(self):
        # подготовка: положить в корзину 2 штуки
        session_item = ShaurmaFactory(price=150)
        url_add = reverse('cart_add', kwargs={'shaurma_id': session_item.id})
        self.client.get(url_add, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.get(url_add, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(Cart.objects.filter(item=session_item).first().quanity, 2)

        url_remove = reverse('cart_remove', kwargs={'shaurma_id': session_item.id})
        resp = self.client.get(url_remove, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 1)

        # второй раз удаляем — позиция должна исчезнуть
        resp2 = self.client.get(url_remove, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertEqual(data2['count'], 0)
        self.assertFalse(Cart.objects.filter(item=session_item).exists())


class CheckoutFlowTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)
        self.item = ShaurmaFactory(price=200)
        # одна позиция в корзине
        self.client.get(
            reverse('cart_add', kwargs={'shaurma_id': self.item.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def test_checkout_page_renders(self):
        resp = self.client.get(reverse('checkout'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Учебная оплата')

    def test_checkout_confirm_creates_order_and_clears_cart(self):
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Order.objects.count(), 0)

        resp = self.client.post(reverse('checkout'), {
            'action': 'confirm',
            'promo_code': '',
        })
        # после подтверждения ожидаем редирект на страницу спасибо
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('checkout_thanks'))

        # корзина очищена
        self.assertEqual(Cart.objects.count(), 0)
        # создан хотя бы один Order
        self.assertGreaterEqual(Order.objects.count(), 1)

        order_row = Order.objects.first()
        self.assertEqual(order_row.user, self.user)
        self.assertEqual(order_row.unit_price, 200)
        self.assertTrue(order_row.order_code)
        self.assertTrue(order_row.is_demo_payment)

    def test_checkout_with_valid_promocode_applies_discount(self):
        promo = Promocode.objects.create(
            code_name='TEST10',
            date_add=timezone.now().date(),
            duration=7,
            discount=10,
        )
        # GET с промокодом
        resp = self.client.get(reverse('checkout'), {'promo': promo.code_name})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'TEST10')

        # POST с подтверждением
        resp2 = self.client.post(reverse('checkout'), {
            'action': 'confirm',
            'promo_code': promo.code_name,
        })
        self.assertEqual(resp2.status_code, 302)

        order_row = Order.objects.first()
        # Проверяем, что применяется скидка 10%
        self.assertEqual(order_row.order_subtotal, 200)
        self.assertEqual(order_row.order_discount, 20)
        self.assertEqual(order_row.order_total, 180)
        self.assertEqual(order_row.promocode, promo)

