from rest_framework import serializers

from member.models import User
from ..models import Comment, Post

__all__ = (
    'CommentSerializer',
)


class SimplePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'pk',
        )


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'profile_img',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    post = SimplePostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'pk',
            'author',
            'post',
            'content',
            'created_date',
        )
        read_only_fields = (
            'author',
            'created_date',
        )
