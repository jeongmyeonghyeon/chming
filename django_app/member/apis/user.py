from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from member.serializer.user import UserCreationSerializer
from utils.permissions import ObjectIsRequestUser
from ..serializer import UserSerializer
from ..models import User

__all__ = (
    'UserListCreateView',
    'UserRetrieveUpdateDestroyView',

    'UserSignupView',
)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer

    # Custom Response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Response를 위한 pk값
        pk = User.objects.get(email=serializer.data['email']).pk
        return Response({"pk": pk}, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    )
