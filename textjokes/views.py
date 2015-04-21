from models import TextJoke, TextPunchline, JokeVotes, TextJokeCategory, \
    TextComment
from serializers import TextJokeSerializer, TextPunchlineSerializer, \
    JokeVoteSerializer, SimpleJokeVoteSerializer, JokeCategorySerializer, \
    TextCommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.db.models import F
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
        'comments': reverse('comment-list', request=request, format=format),
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


class JokeCreate(generics.CreateAPIView):
    # TODO must be implemented
    pass


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
        joke = TextJoke.objects.get(id=request.data.get('joke'))
        if joke.user == request.user:
            return Response({'error': 'You cannot vote on your own joke!'},
                            status=400)
        vote, is_created = JokeVotes.objects.get_or_create(
            joke=joke, user=request.user,
            defaults={'vote': request.data.get('vote', 0)})
        message = 'Thanks'
        joke.score = F('score') + request.data.get('vote')
        joke.save()
        # TODO the logic might need an update to make it less complicated!
        if not is_created:
            if vote.vote != request.data.get('vote'):
                vote.vote += request.data.get('vote')
                if vote.vote == 0:
                    vote.delete()
                    message = 'Bummer!'
                else:
                    vote.save()
            else:
                return Response({'error': 'You have already voted'},
                                status=400)
        return Response({'message': message})


class CommentMixin(object):
    model = TextComment
    serializer_class = TextCommentSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(CommentMixin, self).pre_save(obj)

    def post_save(self, obj):
        obj.user = self.request.user
        super(CommentMixin, self).post_save(obj)


class CommentList(CommentMixin, generics.ListCreateAPIView):
    queryset = TextComment.objects.filter(active=True)
    serializer_class = TextCommentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        joke_saver = TextJoke.objects.get(pk=self.request.data["joke_id"])
        punchline_saver = None
        if self.request.data["punchline_id"]:
            punchline_saver = TextPunchline.objects.get(
                pk=self.request.data["punchline_id"])

        serializer.save(user=self.request.user, joke=joke_saver,
                        punch_line=punchline_saver)