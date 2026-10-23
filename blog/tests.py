from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

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