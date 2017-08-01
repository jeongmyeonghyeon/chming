from rest_framework import generics

from ..serializer import CommentSerializer
from ..models import Comment


__all__ = (
    'CommentCreateView',
)


class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

