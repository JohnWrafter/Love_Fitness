import json
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from openai import OpenAIError

from .models import Post


class BlogPermissionTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='blog-author',
            password='test-password',
        )
        self.other_user = User.objects.create_user(
            username='blog-reader',
            password='test-password',
        )
        self.post = Post.objects.create(
            title='Training Notes',
            title_tag='A sample post',
            author=self.author,
            body='A short training update.',
        )

    def test_anonymous_visitors_cannot_open_blog_management_pages(self):
        for url in (
            reverse('add_blog'),
            reverse('update_blog', args=[self.post.pk]),
            reverse('delete_blog', args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse('account_login'), response.url)

    def test_authenticated_user_can_create_post_as_self(self):
        self.client.force_login(self.author)

        response = self.client.post(reverse('add_blog'), {
            'title': 'New post',
            'title_tag': 'My post',
            'body': 'Post content.',
            'author': self.other_user.pk,
        })

        self.assertRedirects(response, reverse('blog'))
        post = Post.objects.get(title='New post')
        self.assertEqual(post.author, self.author)

    def test_author_can_update_post(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('update_blog', args=[self.post.pk]),
            {
                'title': 'Updated title',
                'title_tag': 'Updated tag',
                'body': 'Updated content.',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated title')

    def test_non_author_cannot_update_or_delete_post(self):
        self.client.force_login(self.other_user)

        update_response = self.client.get(
            reverse('update_blog', args=[self.post.pk]),
        )
        delete_response = self.client.get(
            reverse('delete_blog', args=[self.post.pk]),
        )

        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_author_can_delete_post(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('delete_blog', args=[self.post.pk]),
        )

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_staff_can_update_another_authors_post(self):
        staff_user = User.objects.create_user(
            username='blog-staff',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.get(
            reverse('update_blog', args=[self.post.pk]),
        )

        self.assertEqual(response.status_code, 200)


class ArticleAssistantTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='article-author',
            password='test-password',
        )
        self.article = Post.objects.create(
            title='A beginner guide to strength training',
            title_tag='Start lifting with confidence',
            author=self.author,
            body='Learn the basics of strength training and build a steady habit.',
        )
        self.other_article = Post.objects.create(
            title='Fuel for everyday movement',
            title_tag='Simple nutrition ideas',
            author=self.author,
            body='A few practical meal ideas to support active days.',
        )
        self.valid_data = {
            'query': 'I am new to strength training',
            'consent': 'on',
        }

    def test_fitness_hub_shows_article_assistant_and_existing_articles(self):
        response = self.client.get(reverse('blog'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article assistant')
        self.assertContains(response, 'What would you like to read about?')
        self.assertContains(response, self.article.title)
        self.assertContains(response, reverse('blog_detail', args=[self.article.pk]))

    def test_get_assistant_endpoint_redirects_to_fitness_hub(self):
        response = self.client.get(reverse('article_assistant'))

        self.assertRedirects(response, reverse('blog'))

    @override_settings(OPENAI_API_KEY='')
    @patch('blog.views.OpenAI')
    def test_missing_api_key_does_not_call_provider(self, mock_openai):
        response = self.client.post(reverse('article_assistant'), self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not configured yet')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key', OPENAI_MODEL='test-model')
    @patch('blog.views.OpenAI')
    def test_valid_request_displays_only_catalogued_article_recommendations(
        self,
        mock_openai,
    ):
        mock_client = Mock()
        mock_client.responses.create.return_value = Mock(
            output_text=json.dumps({
                'recommendations': [{
                    'post_id': self.article.pk,
                    'reason': 'A useful introduction to getting started with strength training.',
                }],
            }),
        )
        mock_openai.return_value = mock_client

        response = self.client.post(reverse('article_assistant'), self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Articles for you')
        self.assertContains(response, self.article.title)
        self.assertContains(
            response,
            reverse('blog_detail', args=[self.article.pk]),
        )
        self.assertContains(response, self.other_article.title)
        self.assertEqual(response.content.count(b'class="article-match"'), 1)

        request_payload = mock_client.responses.create.call_args.kwargs
        self.assertEqual(request_payload['model'], 'test-model')
        self.assertEqual(request_payload['max_output_tokens'], 1200)
        self.assertFalse(request_payload['store'])
        self.assertEqual(
            request_payload['text']['format']['name'],
            'article_recommendations',
        )
        self.assertTrue(request_payload['text']['format']['strict'])
        user_payload = json.loads(request_payload['input'][1]['content'])
        self.assertEqual(
            user_payload['visitor_request'],
            self.valid_data['query'],
        )
        self.assertEqual(
            {item['post_id'] for item in user_payload['available_articles']},
            {self.article.pk, self.other_article.pk},
        )
        self.assertNotIn('author', request_payload['input'][1]['content'])

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('blog.views.OpenAI')
    def test_no_consent_does_not_call_provider(self, mock_openai):
        response = self.client.post(
            reverse('article_assistant'),
            {**self.valid_data, 'consent': ''},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'agree before searching')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('blog.views.OpenAI')
    def test_unknown_article_ids_are_not_displayed(self, mock_openai):
        mock_openai.return_value.responses.create.return_value = Mock(
            output_text=json.dumps({
                'recommendations': [{
                    'post_id': 999999,
                    'reason': 'An invented article.',
                }],
            }),
        )

        response = self.client.post(reverse('article_assistant'), self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'We could not find a close match')
        self.assertNotContains(response, 'An invented article.')

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('blog.views.OpenAI')
    def test_no_articles_does_not_call_provider(self, mock_openai):
        Post.objects.all().delete()

        response = self.client.post(reverse('article_assistant'), self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no Fitness Hub articles to search yet')
        mock_openai.assert_not_called()

    @override_settings(OPENAI_API_KEY='test-key')
    @patch('blog.views.OpenAI', side_effect=OpenAIError('provider unavailable'))
    def test_provider_failure_is_reported(self, mock_openai):
        with self.assertLogs('blog.views', level='ERROR'):
            response = self.client.post(
                reverse('article_assistant'),
                self.valid_data,
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'could not find relevant articles')
        mock_openai.assert_called_once()