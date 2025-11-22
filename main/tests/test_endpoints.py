from django.test import TestCase
from django.urls import reverse

from main.factories import (
    ShaurmaFactory,
    StockFactory,
    UserFactory,
)


class PublicPagesTest(TestCase):
    def test_public_pages_ok(self):
        urls = [
            'index', 'catalog', 'about', 'docs', 'privacy_policy', 'user_agreement', 'user_consent',
            'license', 'add_license_1', 'san_rules', 'codex', 'decree', 'feedback', 'locations', 'news',
            'login', 'reg', 'stocks'
        ]
        for name in urls:
            with self.subTest(name=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 200)

    def test_search(self):
        ShaurmaFactory(name='Говяжья')
        resp = self.client.get(reverse('search'), {'search': 'Гов'})
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.get(reverse('search'))
        self.assertEqual(resp2.status_code, 200)


class CatalogAndDetailsTest(TestCase):
    def test_product_detail(self):
        item = ShaurmaFactory()
        resp = self.client.get(reverse('product', kwargs={'slug': item.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_stocks_list_and_detail(self):
        stock = StockFactory()
        resp_list = self.client.get(reverse('stocks'))
        self.assertEqual(resp_list.status_code, 200)
        resp_detail = self.client.get(reverse('stock', kwargs={'slug': stock.slug}))
        self.assertEqual(resp_detail.status_code, 200)


class AjaxBranchesTest(TestCase):
    def test_address_ajax(self):
        resp = self.client.get(reverse('locations'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)

    def test_feedback_ajax(self):
        resp = self.client.get(reverse('feedback'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)


class UserPagesTest(TestCase):
    def test_user_profile_open(self):
        user = UserFactory(is_open=True)
        resp = self.client.get(reverse('user', kwargs={'username': user.username}))
        self.assertEqual(resp.status_code, 200)

    def test_user_profile_closed_for_stranger(self):
        user = UserFactory(is_open=False)
        resp = self.client.get(reverse('user', kwargs={'username': user.username}))
        # redirect to user_closed
        self.assertEqual(resp.status_code, 302)

    def test_user_profile_owner_can_view(self):
        user = UserFactory(is_open=False)
        self.client.force_login(user)
        resp = self.client.get(reverse('user', kwargs={'username': user.username}))
        self.assertEqual(resp.status_code, 200)


class AuthFlowTest(TestCase):
    def test_logout_redirects(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)

    def test_login_get_and_reg_get(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
        self.assertEqual(self.client.get(reverse('reg')).status_code, 200)

    def test_login_with_client_login_helper(self):
        user = UserFactory(password='secret123')
        logged_in = self.client.login(username=user.username, password='secret123')
        self.assertTrue(logged_in)
