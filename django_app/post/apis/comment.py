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


class CommentDestroyView(generics.DestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def delete(self, request, *args, **kwargs):
        instance = Comment.objects.get(pk=self.kwargs['pk'])
        group_instance = Group.objects.get(pk=self.kwargs['group_pk'])

        if request.user == instance.author or request.user == group_instance.author:
            instance.delete()
        else:
            raise APIException({"detail": "권한이 없습니다."})
        ret = {
            "detail": "댓글이 삭제되었습니다."
        }
        return Response(ret)
