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
        fields = ('username', 'display_name', 'email', 'is_verified', 'avatar')

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.get(pk=user.pk)

"""
username = models.CharField(_('username'), max_length=254, unique=True)
display_name = models.CharField(_('display_name'), max_length=254, null=True, blank=True)
email = models.EmailField(_('email address'), max_length=254)
first_name = models.CharField(_('first name'), max_length=30, blank=True)
last_name = models.CharField(_('last name'), max_length=30, blank=True)
avatar = models.URLField(_('avatar url'), max_length=255, blank=True)
is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as '
is_verified = models.BooleanField(_('verified'), default=False, help_text=_('Designates whether the user has been verified via an email confirmation.'))
date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
verified_on = models.DateTimeField(_('verified on'), blank=True, null=True)
objects = CustomUserManager()
"""
