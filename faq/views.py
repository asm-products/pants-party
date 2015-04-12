from rest_framework import generics
from serializers import FAQSerializer
from models import FAQ


class FAQList(generics.ListAPIView):
    queryset = FAQ.objects.filter(active=True)
    serializer_class = FAQSerializer
