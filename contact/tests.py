from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactFormTests(TestCase):
    def test_invalid_submission_renders_form_errors_without_server_error(self):
        response = self.client.post(reverse('contact'), {
            'full_name': '',
            'subject': '',
            'email': 'not-an-email',
            'message': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address')
        self.assertEqual(Contact.objects.count(), 0)

    def test_valid_submission_is_saved_and_redirects(self):
        response = self.client.post(reverse('contact'), {
            'full_name': 'Taylor Test',
            'subject': 'Question',
            'email': 'taylor@example.com',
            'message': 'Please contact me.',
        })

        self.assertRedirects(response, reverse('contact'))
        self.assertTrue(
            Contact.objects.filter(email='taylor@example.com').exists()
        )