from django.contrib.auth import get_user_model
from rest_framework import serializers
from models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('question', 'answer', 'created', 'updated')
        queryset = FAQ.objects.filter(active=True)
