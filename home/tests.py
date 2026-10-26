import json
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from openai import OpenAIError


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