from rest_framework import serializers

from group.serializer.group import GroupSerializer
from member.serializer import UserSerializer
from ..serializer.comment import CommentSerializer
from ..models import Post


__all__ = (
    'PostSerializer',
)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'img',
            'title',
            'content',
            'comments',
        )
        read_only_fields = (
            'author',
            'group',
        )
