from django.test import TestCase

from rest_framework.test import APIClient

from .models import FAQ


class FAQTestCase(TestCase):
    def setUp(self):
        self.question1 = FAQ.objects.create(question='Why?',
                                            answer='Because...')
        self.question2 = FAQ.objects.create(question='Why?',
                                            answer='Because...', active=False)
        self.question3 = FAQ.objects.create(question='Where?',
                                            answer='there...')

    def test_faqs_created(self):
        faqs = FAQ.objects.all()
        self.assertEqual(faqs.count(), 3)

    def test_faq_active(self):
        faqs = FAQ.objects.filter(active=False)
        self.assertEquals(faqs.count(), 1)

    def test_faq_slug(self):
        faqs = FAQ.objects.filter(question='Why?')
        self.assertNotEquals(faqs[0].slug, faqs[1].slug)

    def test_faqs_via_api(self):
        client = APIClient()
        response = client.get('/api/faq/')
        self.assertEquals(len(response.data), 2)
        faq1 = response.data[0]
        faq2 = response.data[1]

        self.assertEquals(faq1["question"], self.question1.question)
        self.assertEquals(faq2["question"], self.question3.question)