from django.shortcuts import render

from models import TextJoke, TextPunchline, JokeVotes
from serializers import TextJokeSerializer, TextPunchlineSerializer, JokeVoteSerializer, SimpleJokeVoteSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import exception_handler
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

@csrf_exempt
@api_view(('GET','POST',))
def api_root(request, format=None):
    return Response({
        'users':        reverse('user-list', request=request, format=format),
        'jokes':        reverse('joke-list', request=request, format=format),
        'votes':        reverse('joke-votes', request=request, format=format),
        'punchlines':   reverse('punchline-list', request=request, format=format),
    })

class JokeMixin(object):
    model = TextJoke
    serializer_class = TextJokeSerializer

    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.user = self.request.user
        return super(JokeMixin, self).pre_save(obj)

class JokeList(JokeMixin, generics.ListCreateAPIView):
    queryset = TextJoke.objects.filter(active=True)
    serializer_class = TextJokeSerializer
    authentication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JokeDetail(generics.RetrieveAPIView):
    queryset = TextJoke.objects.filter(active=True)
    serializer_class = TextJokeSerializer
    authentication_classes = (TokenAuthentication, )

    def pre_save(self, obj):
        print "JokeDetail pre_save()"
        print self.request.user
        obj.user = self.request.user
        super(JokeDetail, self).pre_save(obj)

    def post(self, request, *args, **kwargs):
        print "JokeDetail post"
        user = self.request.user
        if request.user:
            user    = request.user

        if request.user.pk:
            return Response({"message": "User is logged in as %s!" % (request.user.username), "data": request.data})
        else:
            return Response({'detail' : "Not authenticated"}, status = 401)

class PunchlineMixin(object):
    model = TextPunchline
    serializer_class = TextPunchlineSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(PunchlineMixin, self).pre_save(obj)

class PunchlineList(PunchlineMixin, generics.ListCreateAPIView):
    queryset = TextPunchline.objects.filter(active=True)
    serializer_class = TextPunchlineSerializer
    authentication_classes = (TokenAuthentication, )

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
    authentication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        print "JokeVoteList perform_create"
        print "\n\nSelf:"
        print self.request.data

        print "\n\nSerializer:" 
        print serializer.context.keys()
        print dir(serializer)

        print "\n\nRoot:" 
        print serializer.root.data
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        print "JokeVote post"
        print dir(self)
    
        joke = TextJoke.objects.get(pk=request.data["joke"])
        print "\n\nJoke:"
        print joke

        user = self.request.user
        if request.user:
            user    = request.user
        joke = joke

        vote        = JokeVotes()
        vote.user   = request.user
        vote.joke   = joke
        vote.vote   = "1"
        # vote.save()

        serializer = SimpleJokeVoteSerializer(vote)
        print serializer.data
        return Response(serializer.data)
        """
        if request.user.pk:
            return Response({"message": "User is logged in as %s!" % (request.user.username), "data": request.data})
        else:
            return Response({'detail' : "Not authenticated"}, status = 401)
        """



class JokeDetail(generics.RetrieveAPIView):
    queryset = JokeVotes.objects.all()
    serializer_class = JokeVoteSerializer
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        print "JokeDetail post"
        user = self.request.user
        if request.user:
            user    = request.user

        if request.user.pk:
            return Response({"message": "User is logged in as %s!" % (request.user.username), "data": request.data})
        else:
            return Response({'detail' : "Not authenticated"}, status = 401)

