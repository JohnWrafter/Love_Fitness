from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from checkout.models import Order


class OrderAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='order-owner',
            password='test-password',
        )
        self.other_user = User.objects.create_user(
            username='other-user',
            password='test-password',
        )
        self.order = Order.objects.create(
            full_name='Order Owner',
            email='owner@example.com',
            phone_number='123456789',
            country='GB',
            town_or_city='London',
            street_address1='1 Test Street',
            original_bag='{}',
            stripe_pid='pi_test',
        )
        self.order.user_profile = self.owner.userprofile
        self.order.save()

    def test_profile_redirects_anonymous_visitors_to_login(self):
        response = self.client.get(reverse('profile'))

        self.assertRedirects(
            response,
            f'{reverse("account_login")}?next={reverse("profile")}',
        )

    def test_order_history_requires_login(self):
        response = self.client.get(
            reverse('order_history', args=[self.order.order_number]),
        )

        self.assertRedirects(
            response,
            f'{reverse("account_login")}?next='
            f'{reverse("order_history", args=[self.order.order_number])}',
        )

    def test_owner_can_view_order_history(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse('order_history', args=[self.order.order_number]),
        )

        self.assertEqual(response.status_code, 200)

    def test_another_user_cannot_view_order_history(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse('order_history', args=[self.order.order_number]),
        )

        self.assertEqual(response.status_code, 404)

    def test_checkout_success_requires_order_owner(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse('checkout_success', args=[self.order.order_number]),
        )

        self.assertEqual(response.status_code, 404)

    def test_guest_checkout_success_requires_matching_session_order(self):
        response = self.client.get(
            reverse('checkout_success', args=[self.order.order_number]),
        )

        self.assertEqual(response.status_code, 404)

    def test_guest_can_view_own_checkout_success(self):
        session = self.client.session
        session['checkout_order_number'] = self.order.order_number
        session.save()

        response = self.client.get(
            reverse('checkout_success', args=[self.order.order_number]),
        )

        self.assertEqual(response.status_code, 200)