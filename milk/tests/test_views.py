from django.test import TestCase
from django.urls import reverse

from ..models import Post, Comment


class CommentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 comments for pagination tests
        number_of_comments = 13

        for comment_id in range(number_of_comments):
            Comment.objects.create(
                body=f'Thats my opinion',
            )

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('post_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'milk/post_detail.html')
