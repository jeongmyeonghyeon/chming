from rest_framework import generics

from group.serializer.region import RegionSerializer
from ..models import Region

__all__ = (
    'RegionListCreateView',
)


class RegionListCreateView(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class RegionUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
