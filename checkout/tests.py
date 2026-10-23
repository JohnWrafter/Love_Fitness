from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

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
        create_intent.assert_called_once()

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