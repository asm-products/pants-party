from django.forms import widgets
from rest_framework import serializers
from models import TextJoke, TextPunchline
from ppuser.serializers import UserSerializer
# from django.contrib.auth.models import User
from django.conf import settings

class TextPunchlineSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)

    def perform_create(self, serializer):
        print "Perform_create"
        instance = serializer.save(user=self.request.user)

    def get_validation_exclusions(self):
        print "Validate"
        exclusions = super(TextPunchlineSerializer, self).get_validation_exclusions()
        return exclusions + ['user']

    class Meta:
        model = TextPunchline
        fields = ('id', 'user', 'text', 'created', 'active', 'responses', 'score')

class TextJokeSerializer(serializers.ModelSerializer):
    user            = UserSerializer(read_only=True, many=False)
    punchlines      = TextPunchlineSerializer(read_only=True, many=True)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)

    def get_validation_exclusions(self):
        exclusions = super(TextJokeSerializer, self).get_validation_exclusions()
        return exclusions + ['user']

    class Meta:
        model = TextJoke
        fields = ('id', 'user', 'punchlines', 'text', 'created', 'active', 'responses', 'score')
