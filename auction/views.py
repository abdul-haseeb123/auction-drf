from django.shortcuts import render
from auction.models import User
from auction.serializers import UserSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
# Create your views here.

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
         # Handle other field updates
        allowed_fields = ['first_name', 'last_name']  # Add or remove fields as needed
        partial_data = {k: v for k, v in request.data.items() if k in allowed_fields}

        serializer = self.get_serializer(instance, data=partial_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    try:
        current_password = request.data["current_password"]
        new_password = request.data["new_password"]
    except KeyError:
        return Response("Invalid data given", status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(email=request.user)

    if not user.check_password(current_password):
        return Response("Invalid data given", status=status.HTTP_400_BAD_REQUEST)
    if len(new_password) == 0:
        return Response("new password cannot be empty", status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({"success": True, "message": "Password updated successfully"})