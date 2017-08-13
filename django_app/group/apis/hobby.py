from rest_framework import generics

from group.serializer.hobby import HobbySerializer
from ..models import Hobby


class HobbyListView(generics.ListAPIView):
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer
