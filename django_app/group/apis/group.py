from rest_framework import generics, permissions

from group.serializer.group import GroupSerializer
from utils.permissions import AuthorIsRequestUser
from ..models import Group


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
    pass
    # serializer_class = GroupSerializer
    #
    # def get_queryset(self):
    #     # request 된 좌표값 (현재좌표)
    #     lat1 = float(self.request.GET['lat'])
    #     lng1 = float(self.request.GET['lng'])
    #     distance_limit = 0.5
    #
    #     groups = Group.objects.iterator()
    #     filter_group_pk_list = []
    #     for group in groups:
    #         distance = distance_func(lat1, lng1)
    #         if distance > distance_limit:
    #             filter_group_pk_list.append(group.pk)
    #
    #     return Group.objects.filter(pk__in=filter_group_pk_list)


        # print('@@@@@ lat: ', lat1, ' @@@@@: lng: ', lng1)
        #
        # # 특정그룹의 좌표값
        # g = Group.objects.get(pk=1)
        # lat2 = g.lat
        # lng2 = g.lng
        # print('@@@@@ lat2: ', lat2, ' @@@@@: lng2: ', lng2)
        #
        # # 두 좌표사이의 거리 계산
        # print('distance = ', distance_func(lat1, lng1, lat2, lng2))
        #
        # # 반환값...
        # list = []
        # if distance_func(lat1, lng1, lat2, lng2) > 0.5:
        #     list.append(Group.objects.get(pk=1))
        #     print(list)
        # else:
        #     pass
