from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from itertools import chain

from group.models import Group
from utils.permissions import AuthorIsRequestUser
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

    def list(self, request, *args, **kwargs):
        group = Group.objects.filter(pk=self.kwargs['group_pk'])
        post = Post.objects.filter(group=group)
        notice = Post.objects.filter(group=group).exclude(
            post_type='False').order_by('-modified_date')[:2]

        # 쿼리셋이 아닌 리스트형식도 반환가능
        # 쿼리셋을 리스트로 변환하고 chain 으로 묶어준다
        queryset = list(chain(notice, post))

        if queryset[:2] == queryset[2:4] or queryset[:2] == queryset[2:4][::-1]:
            queryset = post
        elif queryset[0] or queryset[1] == queryset[2]:
            queryset = list(chain(notice, post[1:]))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

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
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def delete(self, request, *args, **kwargs):
        instance = Post.objects.get(pk=self.kwargs['pk'])

        if request.user == instance.author:
            instance.delete()
        else:
            raise APIException({"detail": "권한이 없습니다."})
        ret = {
            "detail": "게시글이 삭제되었습니다."
        }
        return Response(ret)


class PostLikeToggleView(APIView):
    def post(self, request, group_pk, pk):
        instance = get_object_or_404(Post, pk=pk)
        post_like, post_like_created = instance.postlike_set.get_or_create(
            user=request.user
        )
        if not post_like_created:
            post_like.delete()
        return Response({'created': post_like_created})
