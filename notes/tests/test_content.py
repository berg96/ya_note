from django.test import TestCase
from django.urls import reverse

from notes.models import Note, User


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='IamGroot')
        Note.objects.bulk_create(
            Note(
                title=f'Note{index}',
                text='Pro100 Text',
                author=cls.author,
                slug=f'note{index}'
            )
            for index in range(2)
        )

    def test_notes_count(self):
        self.client.force_login(self.author)
        self.assertEqual(
            len(self.client.get(reverse('notes:list')).context['object_list']),
            Note.objects.filter(author=self.author).count()
        )
