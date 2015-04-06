from django.shortcuts import render

from models import BlogPost
from serializers import BlogPostSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import exception_handler
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt

class BlogMixin(object):
    model = BlogPost
    serializer_class = BlogPostSerializer

class BlogPostList(BlogMixin, generics.ListCreateAPIView):
    queryset                = BlogPost.objects.all()
    serializer_class        = BlogPostSerializer
    authentication_classes  = (TokenAuthentication, )
    lookup_field            = "slug"
    lookup_url_kwarg        = "slug"

class BlogPostDetail(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = (TokenAuthentication, )
    lookup_field            = "slug"
    lookup_url_kwarg        = "slug"
