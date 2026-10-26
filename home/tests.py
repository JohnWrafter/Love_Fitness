import json
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from openai import OpenAIError

from products.models import Category, Product


def workout_output():
    return {
        'title': 'Beginner strength routine',
        'weekly_schedule': [
            {
                'day': day,
                'focus': f'Session {day}',
                'warm_up': ['Easy marching'],
                'exercises': [{
                    'name': 'Chair squat',
                    'sets': 2,
                    'reps_or_duration': '8 reps',
                    'rest': '60 seconds',
                }],
            }
            for day in range(1, 4)
        ],
        'progression': 'Add repetitions gradually when comfortable.',
    }


def nutrition_output():
    return {
        'title': 'Simple vegetarian meal ideas',
        'meals': [
            {
                'meal_number': meal_number,
                'name': f'Meal {meal_number}',
                'description': 'A balanced everyday meal.',
                'ingredients': ['Oats', 'Berries'],
                'preparation': 'Combine and serve.',
            }
            for meal_number in range(1, 4)
        ],
        'note': 'Check ingredient labels for allergens.',
    }


class WorkoutRoutineViewTests(TestCase):
    valid_data = {
        'goal': 'build_strength',
        'experience': 'beginner',
        'days_per_week': '3',
        'duration': '45',
        'equipment': 'Dumbbells and resistance bands',
        'location': 'home',
        'limitations': '',
        'consent': 'on',
    }

    def test_workout_builder_form_is_available(self):
        response = self.client.get('/workout-routine/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Workout Builder')
        self.assertContains(response, 'Injuries or physical limitations')

    @override_settings(OPENAI_API_KEY='')
    @patch('home.views.OpenAI')
    def test_missing_api_key_shows_configuration_error(self, mock_openai):
        response = self.client.post('/workout-routine/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not configured yet')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key', OPENAI_MODEL='test-model')
    @patch('home.views.OpenAI')
    def test_valid_form_generates_and_displays_routine(self, mock_openai):
        mock_client = Mock()
        mock_client.responses.create.return_value = Mock(
            output_text=json.dumps(workout_output()),
        )
        mock_openai.return_value = mock_client

        response = self.client.post('/workout-routine/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your workout routine')
        self.assertContains(response, 'Day 1: Session 1')
        self.assertContains(response, 'Chair squat')
        mock_openai.assert_called_once_with(api_key='test-key', timeout=30)
        request_payload = mock_client.responses.create.call_args.kwargs
        self.assertEqual(request_payload['model'], 'test-model')
        self.assertEqual(request_payload['max_output_tokens'], 3000)
        self.assertFalse(request_payload['store'])
        self.assertEqual(
            request_payload['text']['format']['type'],
            'json_schema',
        )
        self.assertEqual(
            request_payload['text']['format']['name'],
            'workout_routine',
        )
        self.assertTrue(request_payload['text']['format']['strict'])

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_workout_with_wrong_number_of_sessions_is_not_displayed(self, mock_openai):
        output = workout_output()
        output['weekly_schedule'].pop()
        mock_openai.return_value.responses.create.return_value = Mock(
            output_text=json.dumps(output),
        )

        with self.assertLogs('home.views', level='WARNING'):
            response = self.client.post('/workout-routine/', self.valid_data)

        self.assertContains(response, 'could not generate a routine')
        self.assertNotContains(response, 'Your workout routine')

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_invalid_form_does_not_call_provider(self, mock_openai):
        invalid_data = {**self.valid_data, 'days_per_week': '8'}

        response = self.client.post('/workout-routine/', invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_provider_is_not_called_without_data_sharing_consent(self, mock_openai):
        data_without_consent = {**self.valid_data, 'consent': ''}

        response = self.client.post('/workout-routine/', data_without_consent)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI', side_effect=OpenAIError('provider unavailable'))
    def test_provider_failure_is_reported(self, mock_openai):
        with self.assertLogs('home.views', level='ERROR'):
            response = self.client.post('/workout-routine/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'could not generate a routine')
        mock_openai.assert_called_once()


class NutritionPlanViewTests(TestCase):
    valid_data = {
        'goal': 'balanced',
        'preferences': 'Vegetarian',
        'restrictions': 'Peanuts',
        'meals_per_day': '3',
        'cooking_time': '30 minutes',
        'budget': 'budget-friendly',
        'consent': 'on',
    }

    def test_nutrition_builder_form_is_available(self):
        response = self.client.get('/nutrition-plan/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Nutrition Planner')
        self.assertContains(response, 'Food allergies or restrictions')
        self.assertContains(response, 'not medical advice')

    @override_settings(OPENAI_API_KEY='')
    @patch('home.views.OpenAI')
    def test_missing_api_key_shows_configuration_error(self, mock_openai):
        response = self.client.post('/nutrition-plan/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not configured yet')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key', OPENAI_MODEL='test-model')
    @patch('home.views.OpenAI')
    def test_valid_form_generates_and_displays_general_meal_ideas(self, mock_openai):
        mock_client = Mock()
        mock_client.responses.create.return_value = Mock(
            output_text=json.dumps(nutrition_output()),
        )
        mock_openai.return_value = mock_client

        response = self.client.post('/nutrition-plan/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your meal plan ideas')
        self.assertContains(response, 'Meal 1: Meal 1')
        self.assertContains(response, 'Oats')
        mock_openai.assert_called_once_with(api_key='test-key', timeout=30)
        request_payload = mock_client.responses.create.call_args.kwargs
        self.assertEqual(request_payload['model'], 'test-model')
        self.assertFalse(request_payload['store'])
        self.assertEqual(
            request_payload['text']['format']['name'],
            'nutrition_plan',
        )
        self.assertTrue(request_payload['text']['format']['strict'])
        self.assertIn('Peanuts', request_payload['input'][1]['content'])
        self.assertIn('calorie counts', request_payload['input'][0]['content'])

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_nutrition_plan_with_wrong_number_of_meals_is_not_displayed(
        self,
        mock_openai,
    ):
        output = nutrition_output()
        output['meals'].pop()
        mock_openai.return_value.responses.create.return_value = Mock(
            output_text=json.dumps(output),
        )

        with self.assertLogs('home.views', level='WARNING'):
            response = self.client.post('/nutrition-plan/', self.valid_data)

        self.assertContains(response, 'could not generate a meal plan')
        self.assertNotContains(response, 'Your meal plan ideas')

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_provider_is_not_called_without_data_sharing_consent(self, mock_openai):
        data_without_consent = {**self.valid_data, 'consent': ''}

        response = self.client.post('/nutrition-plan/', data_without_consent)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_invalid_form_does_not_call_provider(self, mock_openai):
        invalid_data = {**self.valid_data, 'meals_per_day': '10'}

        response = self.client.post('/nutrition-plan/', invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI', side_effect=OpenAIError('provider unavailable'))
    def test_provider_failure_is_reported(self, mock_openai):
        with self.assertLogs('home.views', level='ERROR'):
            response = self.client.post('/nutrition-plan/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'could not generate a meal plan')
        mock_openai.assert_called_once()


class ProductFinderViewTests(TestCase):
    def setUp(self):
        self.equipment = Category.objects.create(
            name='fitness_equipment',
            friendly_name='Fitness Equipment',
        )
        self.apparel = Category.objects.create(
            name='leggings',
            friendly_name='Leggings',
        )
        self.dumbbells = Product.objects.create(
            category=self.equipment,
            name='Adjustable Dumbbells',
            description='Compact adjustable dumbbells for home workouts.',
            price='34.99',
            stock_quantity=4,
            colour='Black',
        )
        self.leggings = Product.objects.create(
            category=self.apparel,
            name='Training Leggings',
            description='Stretch fabric leggings for training.',
            price='24.99',
            stock_quantity=2,
        )
        self.out_of_stock = Product.objects.create(
            category=self.equipment,
            name='Out of stock kettlebell',
            description='A kettlebell for strength training.',
            price='19.99',
            stock_quantity=0,
        )
        self.valid_data = {
            'query': 'Home strength training equipment',
            'category': '',
            'max_price': '40.00',
            'consent': 'on',
        }

    def test_product_finder_form_is_available(self):
        response = self.client.get('/product-finder/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Product Finder')
        self.assertContains(response, 'in stock')
        self.assertContains(response, 'sent to OpenAI')
        self.assertContains(response, 'Fitness Equipment')

    @override_settings(OPENAI_API_KEY='')
    @patch('home.views.OpenAI')
    def test_missing_api_key_shows_configuration_error(self, mock_openai):
        response = self.client.post('/product-finder/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not configured yet')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key', OPENAI_MODEL='test-model')
    @patch('home.views.OpenAI')
    def test_recommendations_resolve_to_available_catalogue_products(
        self,
        mock_openai,
    ):
        mock_openai.return_value.responses.create.return_value = Mock(
            output_text=json.dumps({
                'recommendations': [
                    {
                        'product_id': self.dumbbells.pk,
                        'reason': 'Compact equipment suited to home strength sessions.',
                    },
                    {
                        'product_id': self.out_of_stock.pk,
                        'reason': 'Should never be displayed.',
                    },
                    {
                        'product_id': 999999,
                        'reason': 'Should not resolve to a product.',
                    },
                ],
            }),
        )

        response = self.client.post('/product-finder/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Adjustable Dumbbells')
        self.assertContains(response, '£34.99')
        self.assertContains(response, 'View product')
        self.assertNotContains(response, 'Out of stock kettlebell')
        self.assertNotContains(response, 'Should never be displayed')
        self.assertNotContains(response, '999999')

        request_payload = mock_openai.return_value.responses.create.call_args.kwargs
        self.assertEqual(request_payload['model'], 'test-model')
        self.assertFalse(request_payload['store'])
        self.assertEqual(
            request_payload['text']['format']['name'],
            'product_recommendations',
        )
        self.assertTrue(request_payload['text']['format']['strict'])
        catalogue = json.loads(request_payload['input'][1]['content'])
        self.assertEqual(
            catalogue['shopper_request'],
            self.valid_data['query'],
        )
        self.assertEqual(
            [item['product_id'] for item in catalogue['available_catalogue']],
            [self.dumbbells.pk, self.leggings.pk],
        )

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_product_sold_during_generation_is_not_recommended(self, mock_openai):
        provider_response = Mock(
            output_text=json.dumps({
                'recommendations': [{
                    'product_id': self.dumbbells.pk,
                    'reason': 'Useful for strength sessions.',
                }],
            }),
        )

        def sell_product(**kwargs):
            Product.objects.filter(pk=self.dumbbells.pk).update(stock_quantity=0)
            return provider_response

        mock_openai.return_value.responses.create.side_effect = sell_product

        response = self.client.post('/product-finder/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'We could not find a close match')
        self.assertNotContains(response, 'Adjustable Dumbbells')

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_category_and_budget_filter_catalogue_before_sending_to_ai(
        self,
        mock_openai,
    ):
        mock_openai.return_value.responses.create.return_value = Mock(
            output_text=json.dumps({
                'recommendations': [{
                    'product_id': self.dumbbells.pk,
                    'reason': 'Suitable for strength sessions.',
                }],
            }),
        )
        data = {
            **self.valid_data,
            'category': str(self.equipment.pk),
            'max_price': '30.00',
        }

        response = self.client.post('/product-finder/', data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No matching products in stock')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_provider_is_not_called_without_consent(self, mock_openai):
        data_without_consent = {**self.valid_data, 'consent': ''}

        response = self.client.post('/product-finder/', data_without_consent)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI')
    def test_invalid_form_does_not_call_provider(self, mock_openai):
        invalid_data = {**self.valid_data, 'max_price': '-1'}

        response = self.client.post('/product-finder/', invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ensure this value is greater than or equal to 0')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.OpenAI', side_effect=OpenAIError('provider unavailable'))
    def test_provider_failure_is_reported(self, mock_openai):
        with self.assertLogs('home.views', level='ERROR'):
            response = self.client.post('/product-finder/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'could not find product recommendations')
        mock_openai.assert_called_once()