from rest_framework import generics, permissions

from group.serializer.group import GroupSerializer
from utils.permissions import AuthorIsRequestUser
from ..models import Group

__all__ = (
    'MainGroupListView',
)


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )


class MainGroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        # query string 으로 위도, 경도, 반경을 받는다.
        # request.GET 의 키값을 사용
        origin_lat = float(self.request.GET['lat'])
        origin_lng = float(self.request.GET['lng'])
        distance_limit = float(self.request.GET['distance_limit'])
        print('@@@@@@@@@@', origin_lat, origin_lng, distance_limit)
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#iterator
        # 쿼리를 수행하여 QuerySet을 평가하고 결과에 대한 반복자를 반환합니다. ...
        groups = Group.objects.iterator()
        filter_group_pk_list = []
        for group in groups:
            distance = group.get_distance(origin_lat, origin_lng)
            if distance < distance_limit:
                print(distance)
                filter_group_pk_list.append(group.pk)
        print(filter_group_pk_list)
        print('Count@@@@@', Group.objects.count())
        return Group.objects.filter(pk__in=filter_group_pk_list)
