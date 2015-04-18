from django.test import TestCase
from models import BlogPost
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory


class BlogTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.user = get_user_model().objects.create_user(username='bmelton', email='barry.melton@gmail.com', password='top_secret')
        self.factory = APIRequestFactory()

        blog1 = BlogPost(id=1, author=self.user, title="Test Blog Title 1", body="This is a test blog article.")
        blog1.save()

        blog2 = BlogPost(id=2, author=self.user, title="Test Blog Title 2", body="This is another test blog article.")
        blog2.save()

    def test_posts_created(self):
        blogs = BlogPost.objects.all()
        self.assertEqual(blogs.count(), 2)

    def test_posts_via_api(self):
        client = APIClient()
        response = client.get('/api/blogs/')
        blog1 = response.data[0]
        blog2 = response.data[1]

        self.assertEqual(blog1["id"], 1)
        self.assertEqual(blog1["slug"], "test-blog-title-1")

        self.assertEqual(blog2["id"], 2)
        self.assertEqual(blog2["slug"], "test-blog-title-2")
