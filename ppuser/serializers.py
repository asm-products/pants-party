from django.forms import widgets
from rest_framework import serializers
from django.conf import settings
from textjokes.models import TextJoke
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # fields = ('id', 'username', 'jokes')
        fields = ('id', 'username', 'avatar')
