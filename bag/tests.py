from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from products.models import Category, Product
from bag.views import add_to_bag


class BagSessionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(
            name='activewear',
            friendly_name='Activewear'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Performance Leggings',
            description='Soft stretch leggings for training.',
            gender='Women',
            colour='Black',
            has_sizes=True,
            price=49.99,
            stock_quantity=12,
        )
        self.client = Client()

    def _make_request(self, path, data):
        request = self.factory.post(path, data=data)
        request.session = {}
        setattr(request, '_messages', FallbackStorage(request))
        return request

    def test_add_to_bag_handles_size_when_existing_item_is_plain_quantity(self):
        request = self._make_request(
            f'/bag/add/{self.product.id}/',
            {
                'quantity': '2',
                'redirect_url': '/products/',
                'product_size': 'm',
            }
        )
        request.session['bag'] = {str(self.product.id): 1}

        response = add_to_bag(request, self.product.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.session['bag'][str(self.product.id)]['items_by_size']['m'], 2)

    def test_update_button_posts_quantity_to_adjust_bag(self):
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {'items_by_size': {'m': 1}}
        }
        session.save()

        response = self.client.post(
            reverse('adjust_bag', args=[self.product.id]),
            {'quantity': '3', 'product_size': 'm'},
        )

        self.assertRedirects(response, reverse('view_bag'))
        self.assertEqual(
            self.client.session['bag'][str(self.product.id)]
            ['items_by_size']['m'],
            3,
        )

    def test_bag_buttons_render_their_matching_form_actions(self):
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {'items_by_size': {'m': 1}}
        }
        session.save()

        response = self.client.get(reverse('view_bag'))
        html = response.content.decode()

        self.assertContains(
            response,
            f'action="{reverse("adjust_bag", args=[self.product.id])}"',
        )
        self.assertContains(
            response,
            f'formaction="{reverse("remove_from_bag", args=[self.product.id])}"',
        )
        self.assertIn('name="product_size" value="m"', html)

    def test_remove_button_posts_and_redirects_to_updated_bag(self):
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {'items_by_size': {'m': 1}}
        }
        session.save()

        response = self.client.post(
            reverse('remove_from_bag', args=[self.product.id]),
            {'product_size': 'm'},
        )

        self.assertRedirects(response, reverse('view_bag'))
        self.assertNotIn(str(self.product.id), self.client.session['bag'])

    def test_remove_single_size_preserves_other_sizes(self):
        session = self.client.session
        session['bag'] = {
            str(self.product.id): {'items_by_size': {'m': 1, 'l': 2}}
        }
        session.save()

        response = self.client.post(
            reverse('remove_from_bag', args=[self.product.id]),
            {'product_size': 'm'},
        )

        self.assertRedirects(response, reverse('view_bag'))
        self.assertEqual(
            self.client.session['bag'][str(self.product.id)]['items_by_size'],
            {'l': 2},
        )

    def test_remove_endpoint_rejects_get_requests(self):
        response = self.client.get(
            reverse('remove_from_bag', args=[self.product.id]),
        )

        self.assertEqual(response.status_code, 405)
