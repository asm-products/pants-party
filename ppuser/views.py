from models import CustomUser
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from rest_framework.response import Response
from serializers import UserSerializer, MeSerializer
from rest_framework import status
import json


class UsernameAvailable(APIView):
    def get(self, request, *args, **kwargs):
        print kwargs["username"]

        try:
            result = CustomUser.objects.get(username="%s" % kwargs["username"])
            output = {}
            output["available"] = False
        except CustomUser.DoesNotExist:
            output = {}
            output["available"] = True

        return Response(output)


class MeList(APIView):
    serializer_class = MeSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, *args, **kwargs):
        print request.user
        user = request.user
        data =  CustomUser.objects.get(pk=user.pk)
        serializer = MeSerializer(data)
        return Response(serializer.data)
        # queryset = self.get_queryset()

    def post(self, request, format=None):
        # Have to ignore .is_valid() serializer method because of the lack of PK update.
        # It's weird, but what isn't?
        serializer = MeSerializer(data=request.data)

        # Only update current logged-in user, getting username from request
        user = CustomUser.objects.get(pk=request.user.pk)

        # Have to validate to satisfy DRF, but then I'll ignore it.
        temp = serializer.is_valid()

        try: 
            user.username = request.data["username"]
            user.email = request.data["email"]
            user.set_profile = True
            user.save()
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception, e:
            output = {}
            output["error"] = str(e)
            return Response(json.dumps(output), status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Serializer won't validate if username is the same.  That is dumb.  Need to exclude it.
            print "Valid?"
            # TODO - Verify that username is valid and unique
            # TODO - Verify that email address is valid and unique
            # TODO - Send email trigger that email address has changed and needs verification
            # TODO - Ensure that user's "set_profile" field is set True on success
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def pre_save(self, obj):
        obj.user = self.request.user
        super(UserDetail, self).pre_save(obj)

    def post(self, request, *args, **kwargs):
        if request.user.pk:
            return Response({"message": "User is logged in as %s!" % (request.user.username), "data": request.data})
        else:
            return Response({'detail': "Not authenticated"}, status=401)
