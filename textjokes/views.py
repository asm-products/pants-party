from models import TextJoke, TextPunchline, JokeVotes, TextJokeCategory
from serializers import TextJokeSerializer, TextPunchlineSerializer, \
    JokeVoteSerializer, SimpleJokeVoteSerializer, JokeCategorySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
from django.db.models import F


@csrf_exempt
@api_view(('GET', 'POST', ))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'jokes': reverse('joke-list', request=request, format=format),
        'votes': reverse('joke-votes', request=request, format=format),
        'punchlines': reverse('punchline-list', request=request, format=format),
    })


class JokeMixin(object):
    model = TextJoke
    serializer_class = TextJokeSerializer

    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.user = self.request.user
        return super(JokeMixin, self).pre_save(obj)


class JokeCategoryList(JokeMixin, generics.ListCreateAPIView):
    queryset = TextJokeCategory.objects.filter(active=True)
    serializer_class = JokeCategorySerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class JokeList(JokeMixin, generics.ListCreateAPIView):
    queryset = TextJoke.objects.filter(active=True)
    serializer_class = TextJokeSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = TextJoke.objects.filter(active=True)
        category = self.request.QUERY_PARAMS.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset


class JokeDetail(generics.RetrieveAPIView):
    queryset = TextJoke.objects.filter(active=True)
    serializer_class = TextJokeSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def pre_save(self, obj):
        print "JokeDetail pre_save()"
        print self.request.user
        obj.user = self.request.user
        super(JokeDetail, self).pre_save(obj)

    def post(self, request, *args, **kwargs):
        if request.user.pk:
            return Response({"message": "User is logged in as %s!" %
                            (request.user.username), "data": request.data})
        else:
            return Response({'detail': "Not authenticated"}, status=401)


class PunchlineMixin(object):
    model = TextPunchline
    serializer_class = TextPunchlineSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(PunchlineMixin, self).pre_save(obj)


class PunchlineList(PunchlineMixin, generics.ListCreateAPIView):
    queryset = TextPunchline.objects.filter(active=True)
    serializer_class = TextPunchlineSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        saver = TextJoke.objects.get(pk=self.request.data["joke_id"])
        serializer.save(user=self.request.user, joke=saver)

    def pre_save(self, obj):
        obj.user = self.request.user
        super(PunchlineList, self).pre_save(obj)

    def post_save(self, obj):
        obj.user = self.request.user
        super(PunchlineList, self).post_save(obj)


class VoteMixin(object):
    model = JokeVotes
    serializer_class = JokeVoteSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(VoteMixin, self).pre_save(obj)


class JokeVoteList(VoteMixin, generics.ListCreateAPIView):
    queryset = JokeVotes.objects.all()
    serializer_class = JokeVoteSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        joke = TextJoke.objects.get(pk=request.data["joke"])
        vote = JokeVotes()
        try:
            vote.user = request.user
            vote.joke = joke
            vote.vote = "1"
            vote.save()

            joke.score = joke.score + 1
            joke.save()
        except IntegrityError:
            # If a vote for this joke by this user already exists, simply
            # return that joke instead of creating a new one.
            vote = JokeVotes.objects.get(user=request.user, joke=joke)

        serializer = SimpleJokeVoteSerializer(vote)
        return Response(serializer.data)


class JokeVoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JokeVotes.objects.all()
    serializer_class = JokeVoteSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_anonymous() is True:
            # Remove the vote.  TODO, this is very shitty.
            joke = TextJoke.objects.get(pk=kwargs["pk"])
            vote = JokeVotes.objects.get(user=request.user, joke=joke)
            vote.delete()

            # Decrement the vote score
            joke.score = F('score') - 1
            joke.save()

        output = {}
        output["message"] = "Deleted"
        return Response(json.dumps(output))
