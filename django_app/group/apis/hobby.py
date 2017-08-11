from rest_framework import generics

from group.serializer.region import RegionSerializer
from ..models import Hobby


class HobbyListView(generics.ListAPIView):
    queryset = Hobby.objects.all()
    serializer_class = RegionSerializer
