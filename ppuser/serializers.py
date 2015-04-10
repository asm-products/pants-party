from django.contrib.auth import get_user_model
from rest_framework import serializers
from models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'avatar')


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'display_name', 'email', 'set_profile', 'is_verified', 'avatar')

    def get_validation_exclusions(self):
        exclusions = super(MeSerializer, self).get_validation_exclusions()
        return exclusions + ['username', ]

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.get(pk=user.pk)
