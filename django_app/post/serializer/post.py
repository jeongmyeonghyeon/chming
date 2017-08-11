from rest_framework import serializers

from member.models import User
from ..models import Post, Comment

__all__ = (
    'PostSerializer',
    'PostDetailSerializer',
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


class PostDetailSerializer(serializers.ModelSerializer):
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
            # 'hit_count',
        )
        read_only_fields = (
            'author',
        )


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'post_type',
            'title',
            'content',
            'img',
            'author',
            'created_date',
            # 'like_count',
            # 'hit_count',

        )
        read_only_fields = (
            'author',
        )

    # 모델에 없는 필드 추가해서 보내기
    def to_representation(self, instance):
        # 기존 instance 를 받아서
        ret = super().to_representation(instance)
        # 새로 설정할 내용을 작성하고
        comment_count = instance.comment_set.count()
        # [] 에 필드명을 지정해준다.
        ret['comments_count'] = comment_count

        return ret

