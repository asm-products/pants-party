from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from serializers import SubscriptionSerializer


class SubscriptionView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)

        if serializer.is_valid():
            """
            subscription = Subscription()
            subscription.email = request.data["email"]
            subscription.save()
            """
            serializer.save()
            output = serializer.data
            output.update({"message": "Success."})
            return Response(output, status=201)
        else:
            output = {"message": "Duplicate."}
            return Response(output, status=409)
