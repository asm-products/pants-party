from django.shortcuts import render
from models import CustomUser
from serializers import TextJokeSerializer, TextPunchlineSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import exception_handler
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(active=True)
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(active=True)
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )

    def pre_save(self, obj):
        print "PRE SAVING"
        print self.request.user
        obj.user = self.request.user
        super(JokeDetail, self).pre_save(obj)

    def post(self, request, *args, **kwargs):
        print "POST"
        user = self.request.user
        if request.user:
            user    = request.user

        if request.user.pk:
            return Response({"message": "User is logged in as %s!" % (request.user.username), "data": request.data})
        else:
            return Response({'detail' : "Not authenticated"}, status = 401)
