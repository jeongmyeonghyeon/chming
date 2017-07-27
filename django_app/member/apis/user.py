from rest_framework import generics

from ..serializer import UserSerializer
from ..models import User

__all__ = (
    'UserListCreateView',
)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
            # elif self.request.method == 'POST':
            #     return UserCreationSerializer
