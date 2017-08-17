from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from group.serializer.group import GroupSerializer, GroupDetailSerializer, GroupListSerializer
from .group_function import filtered_group_list as get_filtered_group_list
from group.pagination import GroupPagination
from utils.permissions import AuthorIsRequestUser
from ..models import Group

__all__ = (
    'MainGroupListView',
    'AllGroupListView',
    'GroupRegisterView',
    'GroupRetrieveView',
    'GroupUpdateView',
    'GroupDestroyView',
    'GroupLikeToggleView',
    'GroupJoinView',
)


class MainGroupListView(GenericAPIView):
    serializer_class = GroupListSerializer

    def get(self, request, *args, **kwargs):
        serializer = get_filtered_group_list(self)
        return Response(serializer.data)


class AllGroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer


class GroupRegisterView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response({"pk": serializer.data['pk']}, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class GroupRetrieveView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class GroupUpdateView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser
    )

    def put(self, request, group_pk, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = Group.objects.get(pk=group_pk)
        serializer = GroupSerializer(instance, data=request.data, partial=partial)
        if request.user == instance.author:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise APIException({"detail": "권한이 없습니다."})
        ret = {
            "pk": serializer.data['pk']
        }
        return Response(ret)


class GroupDestroyView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def delete(self, request, group_pk):
        instance = Group.objects.get(pk=group_pk)

        if request.user == instance.author:
            instance.delete()
        else:
            raise APIException({"detail": "권한이 없습니다."})
        ret = {
            "detail": "모임이 삭제되었습니다."
        }
        return Response(ret)


class GroupLikeToggleView(APIView):
    def post(self, request, group_pk):
        instance = get_object_or_404(Group, pk=group_pk)
        group_like, group_like_created = instance.grouplike_set.get_or_create(
            user=request.user
        )
        if not group_like_created:
            group_like.delete()
        return Response({'created': group_like_created})


class GroupJoinView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, group_pk):
        instance = get_object_or_404(Group, pk=group_pk)
        if instance.members.filter(pk=request.user.pk):
            raise APIException({'joined': '이미 가입한 모임입니다.'})
        instance.members.add(request.user)
        return Response({'joined': True})


class IsValidNameView(APIView):
    def get(self, request):
        if Group.objects.filter(name=request.GET['name']).exists():
            ret = {'is_valid': False}
        else:
            ret = {'is_valid': True}
        return Response(ret)
