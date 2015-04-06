from django.forms import widgets
from rest_framework import serializers
from ppuser.serializers import UserSerializer
from models import BlogPost
from django.conf import settings

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)

    def perform_create(self, serializer):
        print "Perform_create"
        instance = serializer.save(user=self.request.user)

    def get_validation_exclusions(self):
        print "Validate"
        exclusions = super(TextPunchlineSerializer, self).get_validation_exclusions()
        return exclusions + ['user']

    class Meta:
        model = BlogPost
        fields = ('id', 'author', 'title', 'slug', 'created', 'header_img', )
