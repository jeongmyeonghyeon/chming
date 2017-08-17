from rest_framework import serializers

from member.serializer.user import SimpleUserSerializer
from utils.fields import CustomListField
from ..models import Group
from post.models import Post


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


class GroupSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    # image = serializers.ImageField()

    class Meta:
        model = Group
        fields = (
            'pk',
            'hobby',
            'image',
            'name',
            'description',
            'address',
            'lat',
            'lng',
        )

    def validate(self, data):
        """
        Checks to be sure that the received password and confirm_password
        fields are exactly the same
        """
        if not 'image' in data:
            data['image'] = 'images/no_image.png'
        return data

    def create(self, validated_data):
        """
        Creates the user if validation succeeds
        """
        # is_valid() 를 통해 생성된 validated_data 에서 set_password 를 위한 password 만 pop으로 추출
        group = self.Meta.model(**validated_data)
        group.save()
        author = validated_data['author']
        group.members.add(author)
        return group


class GroupListSerializer(serializers.ModelSerializer):
    hobby = CustomListField()
    author = SimpleUserSerializer(read_only=True)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    members = SimpleUserSerializer(many=True)
    like_users = SimpleUserSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'pk',
            'hobby',
            'name',
            'image',
            'description',
            'address',
            'lat',
            'lng',
            'author',
            'created_date',
            'modified_date',
            'members',
            'like_users',
        )

    # 모델에 없는 필드 추가해서 보내기
    def to_representation(self, instance):
        # 기존 instance 를 받아서
        ret = super().to_representation(instance)
        # 새로 설정할 내용을 작성하고
        like_users_count = instance.get_all_like_users_count()
        member_count = instance.get_all_member_count()
        # group = Group.objects.filter(pk=self.pk)
        # [] 에 필드명을 지정해준다.
        ret['member_count'] = member_count
        ret['like_users_count'] = like_users_count
        return ret


class GroupDetailSerializer(serializers.ModelSerializer):
    hobby = CustomListField()
    author = SimpleUserSerializer(read_only=True)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    members = SimpleUserSerializer(many=True)
    like_users = SimpleUserSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'pk',
            'hobby',
            'name',
            'image',
            'description',
            'address',
            'lat',
            'lng',
            'author',
            'created_date',
            'modified_date',
            'members',
            'like_users',
        )

    # 모델에 없는 필드 추가해서 보내기
    def to_representation(self, instance):
        # 기존 instance 를 받아서
        ret = super().to_representation(instance)
        # 새로 설정할 내용을 작성하고
        like_users_count = instance.get_all_like_users_count()
        member_count = instance.get_all_member_count()
        # group = Group.objects.filter(pk=self.pk)
        # [] 에 필드명을 지정해준다.
        notice = Post.objects.filter(group=self._args[0]).exclude(post_type='False').order_by('-modified_date')[:2]
        ret['notice'] = PostSerializer(notice, many=True).data
        ret['member_count'] = member_count
        ret['like_users_count'] = like_users_count
        return ret


class MainGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'pk',
            'hobby',
            'lat',
            'lng',
        )
