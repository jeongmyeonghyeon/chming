from rest_framework import generics, permissions

from utils.permissions import AuthorIsRequestUser
from ..serializer import CommentSerializer
from ..models import Comment, Post

__all__ = (
    'CommentListView',
    'CommentCreateView',
    'CommentDeleteView',
)


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_pk = self.kwargs['pk']
        post = Post.objects.get(pk=post_pk)
        instance = serializer.save(author=self.request.user, post=post)
        instance.save()

    def get_queryset(self):
        post_pk = self.kwargs['pk']
        post = Post.objects.get(pk=post_pk)
        return Post.objects.filter(post=post)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )
