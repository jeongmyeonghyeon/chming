from rest_framework import generics, permissions

from utils.permissions import ObjectIsRequestUser
from ..models import Post, Comment
from ..serializer import PostSerializer

__all__ = (
    'PostListCreateView',
)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        comment_content = self.request.data.get('comment')
        if comment_content:
            instance.comment_set = Comment.objects.create(
                post=instance,
                author=instance.author,
                content=comment_content,
            )
            instance.save()


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    )
