from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from notes.models import Note, User


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='IceFrog')
        cls.reader = User.objects.create(username='IamGroot')
        cls.note = Note.objects.create(
            title='title',
            text='text',
            author=cls.author,
        )

    def test_pages_availability(self):
        for name in (
                'notes:home',
                'notes:list',
                'users:login',
                'users:logout',
                'users:signup',
        ):
            with self.subTest(name=name):
                if name == 'notes:list':
                    self.client.force_login(self.author)
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                if name == 'notes:list':
                    self.client.logout()

    def test_availability_for_detail_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (
                    'notes:detail',
                    'notes:edit',
                    'notes:delete',
            ):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name, args in (
                ('notes:list', None),
                ('notes:detail', (self.note.slug,)),
                ('notes:edit', (self.note.slug,)),
                ('notes:delete', (self.note.slug,)),
        ):
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                redirect_url = f'{login_url}?next={url}'
                self.assertRedirects(response, redirect_url)
