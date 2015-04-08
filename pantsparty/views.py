from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLogin
from django.shortcuts import render
from django.contrib.auth import get_user_model
from serializers import UserSerializer
from rest_framework import generics


def home(request):
    return render(request, "home.html", {})


class TwitterLogin(SocialLogin):
    adapter_class = TwitterOAuthAdapter


class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
