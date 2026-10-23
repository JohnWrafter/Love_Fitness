from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from requests import RequestException


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
    @patch('home.views.requests.post')
    def test_missing_api_key_shows_configuration_error(self, mock_post):
        response = self.client.post('/workout-routine/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not configured yet')
        mock_post.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key', OPENAI_MODEL='test-model')
    @patch('home.views.requests.post')
    def test_valid_form_generates_and_displays_routine(self, mock_post):
        provider_response = Mock()
        provider_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Day 1: Squats and rows.',
                },
            }],
        }
        mock_post.return_value = provider_response

        response = self.client.post('/workout-routine/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your workout routine')
        self.assertContains(response, 'Day 1: Squats and rows.')
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.kwargs['json']['model'], 'test-model')
        self.assertEqual(mock_post.call_args.kwargs['timeout'], 30)

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.requests.post')
    def test_invalid_form_does_not_call_provider(self, mock_post):
        invalid_data = {**self.valid_data, 'days_per_week': '8'}

        response = self.client.post('/workout-routine/', invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice')
        mock_post.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.requests.post')
    def test_provider_is_not_called_without_data_sharing_consent(self, mock_post):
        data_without_consent = {**self.valid_data, 'consent': ''}

        response = self.client.post('/workout-routine/', data_without_consent)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        mock_post.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('home.views.requests.post', side_effect=RequestException('provider unavailable'))
    def test_provider_failure_is_reported(self, mock_post):
        with self.assertLogs('home.views', level='ERROR'):
            response = self.client.post('/workout-routine/', self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'could not generate a routine')
        mock_post.assert_called_once()