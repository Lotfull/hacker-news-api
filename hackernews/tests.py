# Create your tests here.

from datetime import datetime, timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from hackernews.models import Post


def mock_now():
    return datetime(2019, 11, 23, 11, 15, 0)


def mock_now_min_1():
    return datetime(2019, 11, 23, 11, 15, 0) - timedelta(minutes=1)


def mock_now_min_2():
    return datetime(2019, 11, 23, 11, 15, 0) - timedelta(minutes=2)


class NoPostsTest(TestCase):
    @staticmethod
    def create_post(title="only a test", url="yes, this is only a test"):
        return Post.objects.create(title=title, url=url)

    def test_post_creation(self):
        post = self.create_post()
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.url)

    @mock.patch('django.utils.timezone.now', mock_now)
    def test_posts_list_view_when_no_posts(self):
        url = reverse("posts_view")
        self.assertEqual(url, '/posts')

        resp = self.client.get(url)
        self.assertEqual(30, Post.objects.all().count())
        self.assertEqual(5, len(eval(resp.content)))

    def test_posts_scrap(self):
        from hackernews.api.scrap import scrap
        scrap()

        self.assertEqual(30, Post.objects.all().count())


class PostTestCase(TestCase):
    def setUp(self):
        @mock.patch('django.utils.timezone.now', mock_now_min_2)
        def create_post1():
            return Post.objects.create(title='B_title', url='B_url')

        @mock.patch('django.utils.timezone.now', mock_now_min_1)
        def create_post2():
            return Post.objects.create(title='A_title', url='C_url')

        @mock.patch('django.utils.timezone.now', mock_now)
        def create_post3():
            return Post.objects.create(title='C_title', url='A_url')

        self.posts = [create_post1(), create_post2(), create_post3()]
        created, created_min_1, created_min_2 = mock_now().isoformat() + "Z", mock_now_min_1().isoformat() + "Z", mock_now_min_2().isoformat() + "Z"
        self.post1_exp = {"id": 1, "title": "B_title", "url": "B_url", "created": created_min_2}
        self.post2_exp = {"id": 2, "title": "A_title", "url": "C_url", "created": created_min_1}
        self.post3_exp = {"id": 3, "title": "C_title", "url": "A_url", "created": created}

    def test_posts_list_view_default(self):
        resp = self.client.get('/posts')

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post3_exp,
            self.post2_exp,
            self.post1_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_order_title(self):
        resp = self.client.get('/posts', data={'order': 'title'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post2_exp,
            self.post1_exp,
            self.post3_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_order_url_neg(self):
        resp = self.client.get('/posts', data={'order': '-url'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post2_exp,
            self.post1_exp,
            self.post3_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_order_created_neg(self):
        resp = self.client.get('/posts', data={'order': 'created'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post1_exp,
            self.post2_exp,
            self.post3_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_order_id(self):
        resp = self.client.get('/posts', data={'order': 'id'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post1_exp,
            self.post2_exp,
            self.post3_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_limit(self):
        resp = self.client.get('/posts', data={'limit': '1'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post3_exp
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_offset(self):
        resp = self.client.get('/posts', data={'offset': '1'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post2_exp,
            self.post1_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_offset_neg(self):
        resp = self.client.get('/posts', data={'offset': '-1'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post3_exp,
            self.post2_exp,
            self.post1_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_limit_big(self):
        resp = self.client.get('/posts', data={'limit': '1000'})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post3_exp,
            self.post2_exp,
            self.post1_exp,
        ]
        self.assertEqual(eval(resp.content), expected)

    def test_posts_list_view_force(self):
        resp = self.client.get('/posts', data={'force': True, 'limit': 100})

        self.assertEqual(resp.status_code, 200)
        expected = [
            self.post3_exp,
            self.post2_exp,
            self.post1_exp,
        ]
        result = eval(resp.content)
        self.assertEqual(result[-3:], expected)
        self.assertEqual(len(result), 33)

    def test_posts_update_scrap(self):
        from hackernews.api.scrap import scrap
        scrap()

        self.assertEqual(33, Post.objects.all().count())

