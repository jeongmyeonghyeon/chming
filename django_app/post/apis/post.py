from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from group.models import Group
from utils.permissions import AuthorIsRequestUser, RequestUserIsGroupMeber
from ..models import Post, Comment

from ..serializer import PostSerializer, PostDetailSerializer, PostPagination

__all__ = (
    'PostListView',
    'PostImageListView',
    'PostNoticeListView',
    'PostCreateView',
    'PostRetrieveView',
    'PostUpdateView',
    'PostDestroyView',
    'PostLikeToggleView',
)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        queryset = Post.objects.filter(group=group)
        return queryset


class PostImageListView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group).exclude(post_img='')


class PostNoticeListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group).exclude(
            post_type='False').order_by('-modified_date')[:2]

        # 수정한 날짜 역순 정렬 (현재 model은 생성한 날짜 역순 정렬... null 값이 상위로 오는상황)
        # 최근 2개만 검색하게 (공지가 2개라서 그이상 필요 x)


class PostCreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        # post 의 author 가 group 의 member 인지 검사
        group = Group.objects.filter(pk=self.kwargs['group_pk'])
        if not group.filter(members__in=[self.request.user]).exists():
            raise APIException({"error": "모임의 회원이 아닙니다."})

        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = Group.objects.get(pk=self.kwargs['group_pk'])
        serializer.save(author=self.request.user, group=group)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostRetrieveView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostDestroyView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )


class PostLikeToggleView(APIView):
    def post(self, request, group_pk, pk):
        instance = get_object_or_404(Post, pk=pk)
        post_like, post_like_created = instance.postlike_set.get_or_create(
            user=request.user
        )
        if not post_like_created:
            post_like.delete()
        return Response({'created': post_like_created})
