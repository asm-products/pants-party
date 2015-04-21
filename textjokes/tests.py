from django.test import TestCase

from rest_framework.test import APIClient

from ppuser.models import CustomUser
from .models import TextJoke, TextPunchline, JokeVotes
from rest_framework.authtoken.models import Token


class JokesTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(username='user1', password='secret1')
        self.user2 = CustomUser.objects.create(username='user2', password='secret2')
        self.joke1 = TextJoke.objects.create(user=self.user1, text='joke1')

        self.punchline1 = TextPunchline.objects.create(
            user=self.user1, joke=self.joke1, text='punchline1')

    def post_with_authenticated_client(self, url, data, user=None):
        client = APIClient()
        if not user:
            user = self.user1
        client.force_authenticate(user=user)
        return client.post(url, data)

    def test_joke_creation_via_api(self):
        try:
            token = Token.objects.get(user=self.user1)
        except Exception:
            token = Token(user=self.user1)
            token.save()

        headers = {"Authorization": "Token %s" % (token.key)}
        data = {'user': self.user1, 'text': 'random joke'}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/api/jokes/', data)
        self.assertEquals(response.status_code, 201)

    def test_user_cannot_vote_more_than_once(self):
        vote1 = JokeVotes.objects.create(joke=self.joke1, user=self.user1)
        data = {'joke': self.joke1.id}
        self.post_with_authenticated_client('/api/votes/', data)
        self.assertEquals(
            JokeVotes.objects.filter(
                joke=self.joke1, user=self.user1).count(), 1)
        vote1.delete()

    def test_user_cannot_vote_on_own_joke(self):
        joke1_votes_before = self.joke1.joke_votes.all().count()
        data = {'joke': self.joke1.id}
        self.post_with_authenticated_client('/api/votes/', data,
                                            self.joke1.user)
        joke1_votes_after = self.joke1.joke_votes.all().count()
        self.assertEquals(joke1_votes_before, joke1_votes_after)

    def test_joke_score_increase(self):
        score_before = self.joke1.score
        data = {'joke': self.joke1.id, 'vote': 1}
        self.post_with_authenticated_client('/api/votes/', data, self.user2)
        joke1 = TextJoke.objects.get(id=self.joke1.id)
        score_after = joke1.score
        self.assertEquals(score_after - score_before, 1)

    def test_joke_score_decrease(self):
        score_before = self.joke1.score
        data = {'joke': self.joke1.id, 'vote': -1}
        self.post_with_authenticated_client('/api/votes/', data, self.user2)
        joke = TextJoke.objects.get(id=self.joke1.id)
        score_after = joke.score
        print(score_after, score_before)
        self.assertEquals(score_before - score_after, 1)

    def test_punchline_creation_via_api(self):
        data = {'joke_id': self.joke1.id, 'text': 'punchline1'}
        response = self.post_with_authenticated_client(
            '/api/punchlines/', data)
        self.assertEquals(response.status_code, 201)

    def test_comment_on_joke_creation_via_api(self):
        data = {'joke_id': self.joke1.id, 'punchline_id': '',
                'text': 'comment1'}
        response = self.post_with_authenticated_client('/api/comments/', data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['comment_on'], 'joke')

    def test_comment_on_punchline_creation_via_api(self):
        data = {'joke_id': self.joke1.id, 'punchline_id': self.punchline1.id,
                'text': 'comment1'}
        response = self.post_with_authenticated_client('/api/comments/', data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['comment_on'], 'punchline')
