from rest_framework import generics

from ..models import Post, Comment
from ..serializer import PostSerializer

__all__ = (
    'PostListCreateView',
)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
