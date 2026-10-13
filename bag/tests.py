from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

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
