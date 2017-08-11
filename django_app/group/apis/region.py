from rest_framework import generics

from group.serializer.region import RegionSerializer
from ..models import Region


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
