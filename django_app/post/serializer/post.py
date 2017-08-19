from rest_framework import serializers

from group.models import Group
from member.models import User
from ..models import Post, Comment

__all__ = (
    'PostSerializer',
    'PostDetailSerializer',
)


class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'author',
        )


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'profile_img',
        )


class SimpleCommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'pk',
            'author',
            'content',
            'created_date',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    comment_set = SimpleCommentSerializer(read_only=True, many=True)
    group = SimpleGroupSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'group',
            'pk',
            'post_type',
            'title',
            'content',
            'post_img',
            'author',
            'created_date',
            'modified_date',
            'comment_set',
        )
        read_only_fields = (
            'author',
            'created_date',
            'modified_date',
            'comment_set',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        comment_count = instance.comment_set.count()
        postlike_count = instance.postlike_set.count()
        ret['comments_count'] = comment_count
        ret['post_like_count'] = postlike_count

        return ret


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'post_type',
            'title',
            'content',
            'post_img',
            'author',
            'created_date',
            'modified_date',
        )
        read_only_fields = (
            'author',
            'created_date',
            'modified_date',
            'comment_set',
        )

    # 모델에 없는 필드 추가해서 보내기
    def to_representation(self, instance):
        # 기존 instance 를 받아서
        ret = super().to_representation(instance)
        # 새로 설정할 내용을 작성하고
        comment_count = instance.comment_set.count()
        postlike_count = instance.postlike_set.count()
        # [] 에 필드명을 지정해준다.
        ret['comments_count'] = comment_count
        ret['post_like_count'] = postlike_count

        return ret
