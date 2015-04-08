from models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from rest_framework.response import Response
from serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(active=True)
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(active=True)
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
