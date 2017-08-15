from rest_framework import generics

from group.serializer.hobby import HobbySerializer
from ..models import Hobby


class HobbyListView(generics.ListCreateAPIView):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer


class HobbyUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer
