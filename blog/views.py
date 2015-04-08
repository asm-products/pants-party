from models import BlogPost
from serializers import BlogPostSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics


class BlogMixin(object):
    model = BlogPost
    serializer_class = BlogPostSerializer


class BlogPostList(BlogMixin, generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = (TokenAuthentication, )


class BlogPostDetail(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = (TokenAuthentication, )
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
