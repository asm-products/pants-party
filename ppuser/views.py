from models import CustomUser
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from rest_framework.response import Response
from serializers import UserSerializer, MeSerializer


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
