from rest_framework import serializers
from ppuser.serializers import UserSerializer
from textjokes.serializers import TextPunchlineSerializer
from models import BlogPost


class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True, many=False)

    def perform_create(self, serializer):
        print "Perform_create"
        serializer.save(user=self.request.user)

    def get_validation_exclusions(self):
        print "Validate"
        exclusions = super(TextPunchlineSerializer, self).get_validation_exclusions()
        return exclusions + ['user']

    class Meta:
        model = BlogPost
        fields = ('id', 'author', 'title', 'slug', 'created', 'body', 'header_img', )
