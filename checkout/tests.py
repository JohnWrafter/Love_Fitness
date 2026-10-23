from types import SimpleNamespace
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from checkout.webhook_handler import StripeWH_Handler
from products.models import Category, Product


class CheckoutValidationTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='test-category')
        product = Product.objects.create(
            category=category,
            name='Test product',
            description='Test product description.',
            price='10.00',
            stock_quantity=5,
        )
        session = self.client.session
        session['bag'] = {str(product.pk): 1}
        session.save()

    @patch(
        'checkout.views.stripe.PaymentIntent.create',
        return_value=SimpleNamespace(client_secret='pi_test_secret_new'),
    )
    def test_invalid_order_form_renders_errors_with_new_payment_intent(
        self,
        create_intent,
    ):
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test Customer',
            'email': 'not-an-email',
            'phone_number': '123456789',
            'street_address1': '1 Test Road',
            'street_address2': '',
            'town_or_city': 'London',
            'postcode': 'AB1 2CD',
            'country': 'GB',
            'county': '',
            'client_secret': 'pi_test_secret_old',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address')
        self.assertContains(response, 'pi_test_secret_new')
        create_intent.assert_called_once_with(amount=1100, currency='gbp')

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_post_with_empty_bag_redirects_without_creating_intent(
        self,
        create_intent,
    ):
        session = self.client.session
        session['bag'] = {}
        session.save()

        response = self.client.post(reverse('checkout'), {})

        self.assertRedirects(response, reverse('view_bag'))
        create_intent.assert_not_called()


class OrderConfirmationEmailTests(TestCase):
    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        DEFAULT_FROM_EMAIL='orders@lovefitness.example',
        STRIPE_CURRENCY='gbp',
    )
    def test_order_confirmation_uses_site_brand_currency_and_customer_email(
        self,
    ):
        order = SimpleNamespace(
            full_name='Taylor Test',
            email='taylor@example.com',
            order_number='ORDER-123',
            date='23 October 2026',
            order_total='20.00',
            delivery_cost='2.00',
            grand_total='22.00',
            street_address1='1 Test Road',
            town_or_city='London',
            country='GB',
            phone_number='123456789',
        )

        StripeWH_Handler(None)._send_confirmation_email(order)

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.from_email, 'orders@lovefitness.example')
        self.assertEqual(message.to, ['taylor@example.com'])
        self.assertIn('Love Fitness order', message.body)
        self.assertIn('Order Total: GBP 20.00', message.body)
        self.assertIn('Grand Total: GBP 22.00', message.body)
        self.assertNotIn('Boutique Ado', message.body)