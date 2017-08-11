from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.compat import is_anonymous
from rest_framework.response import Response

from group.serializer.group import GroupSerializer, MainGroupListSerializer
from utils.permissions import AuthorIsRequestUser
from ..models import Group

__all__ = (
    'MainGroupListView',
)


class MainGroupListView(generics.ListAPIView):
    serializer_class = MainGroupListSerializer

    def get_queryset(self):
        # 로그인한 유저의 모임 필터링
        if not is_anonymous(self.request.user):
            user_hobby = self.request.user.hobby
            origin_lat = float(self.request.GET.get('lat', self.request.user.lat))
            origin_lng = float(self.request.GET.get('lng', self.request.user.lng))
            distance_limit = float(self.request.GET.get('distance_limit', 0.5))
            groups = Group.objects.iterator()
            filter_group_pk_list = []
            for group in groups:
                distance = group.get_distance(origin_lat, origin_lng)
                if distance < distance_limit:
                    filter_group_pk_list.append(group.pk)
            return Group.objects.filter(Q(pk__in=filter_group_pk_list), Q(hobby=user_hobby))
        # 비로그인 유저(anonymous user)의 필터링
        else:
            # query string 으로 위도, 경도, 반경을 받는다.
            # request.GET 의 키값을 사용
            # query string 이 없는 경우 설정해 놓은 좌표값(패스트캠퍼스 위치)을 기준 좌표값으로 사용한다.
            origin_lat = float(self.request.GET.get('lat', 37.517547))
            origin_lng = float(self.request.GET.get('lng', 127.018127))
            distance_limit = float(self.request.GET.get('distance_limit', 0.5))
            print('@@@@@ 현재좌표값, 검색반경: ', origin_lat, origin_lng, distance_limit)
            # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#iterator
            # 쿼리를 수행하여 QuerySet을 평가하고 결과에 대한 반복자를 반환합니다. ...
            groups = Group.objects.iterator()
            # 필터링 된 그룹의 pk 를 보관할 리스트 선언
            filter_group_pk_list = []
            # groups 순회
            for group in groups:
                # group 인스턴스의 get_distance(거리계산하는 함수)를 통해 거리받음
                distance = group.get_distance(origin_lat, origin_lng)
                # 주어진 반경보다 작을 경우 필터링 리스트에 pk 값 추가
                if distance < distance_limit:
                    filter_group_pk_list.append(group.pk)
            print('@@@@@ 전체 그룹 수: ', Group.objects.count())
            print('@@@@@ 필터링 된 그룹들의 pk 리스트: ', filter_group_pk_list)
            # __in 을 통해 serializer 에 사용할 queryset 반환
            return Group.objects.filter(pk__in=filter_group_pk_list)


class AllGroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupRegisterView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"pk": serializer.data['pk']}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )
