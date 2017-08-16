from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from group.models import Group
from utils.permissions import AuthorIsRequestUser
from ..serializer import CommentSerializer
from ..models import Comment, Post

__all__ = (
    'CommentListView',
    'CommentCreateView',
    'CommentDestroyView',
)


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def post(self, request, *args, **kwargs):
        group = Group.objects.filter(pk=self.kwargs['group_pk'])
        if not group.filter(members__in=[self.request.user]).exists():
            raise APIException({"error": "모임의 회원이 아닙니다."})

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # queryset = Comment.objects.all()
    # serializer_class = CommentSerializer
    #
    # def perform_create(self, serializer):
    #     post_pk = self.kwargs['pk']
    #     post = Post.objects.get(pk=post_pk)
    #     instance = serializer.save(author=self.request.user, post=post)
    #     instance.save()
    #
    # def get_queryset(self):
    #     post_pk = self.kwargs['pk']
    #     post = Post.objects.get(pk=post_pk)
    #     return Post.objects.filter(post=post)


class CommentDestroyView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )
