from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import generics
from rest_framework.response import Response
from serializers import SubscriptionSerializer
from rest_framework import status
import json
from ppuser.models import CustomUser
from rest_framework import authentication
from rest_framework import exceptions


class AllowAllAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = CustomUser.objects.all()[0]
        return (user, None)


class SubscriptionView(APIView):
    serializer_class = SubscriptionSerializer
    authentication_classes = (AllowAllAuth, )

    def get(self, request, *args, **kwargs):
        """
        print request.user
        user = request.user
        data = CustomUser.objects.get(pk=user.pk)
        serializer = MeSerializer(data)
        """
        output = {}
        output["message"] = "Nothing here."
        return Response(output)

    def post(self, request, format=None):
        serializer = SubscriptionSerializer(data=request.data)

        print request.data
        if serializer.is_valid():
            """
            subscription = Subscription()
            subscription.email = request.data["email"]
            subscription.save()
            """
            serializer.save()
            output = {}
            output["message"] = "Success."
            return Response(serializer.data, status=201)
        else:
            print serializer.errors
            output = {}
            output["message"] = "Duplicate."
            return Response(output, status=409)
