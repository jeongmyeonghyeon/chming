from rest_framework import serializers

from member.models import User
from ..models import Post, Comment


__all__ = (
    'PostSerializer',
)


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            # 'nickname',
        )


class SimpleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'pk',
            'content',
            'created_date',
        )


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    comment_set = SimpleCommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'post_type',
            'title',
            'content',
            'img',
            'author',
            'comment_set',
            'created_date',
            # 'like_count',
            # 'comments_count',
            # 'hit_count',

        )
        read_only_fields = (
            'author',
        )
