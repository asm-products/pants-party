from rest_framework import generics
from rest_framework.response import Response
from serializers import FAQSerializer
from rest_framework import status
from models import FAQ
import json


class FAQList(generics.ListAPIView):
    queryset = FAQ.objects.filter(active=True)
    serializer_class = FAQSerializer
