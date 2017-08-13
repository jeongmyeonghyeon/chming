from rest_framework import serializers

from member.serializer import UserSerializer
from member.serializer.user import SimpleUserSerializer, UserPKSerializer
from utils.fields import CustomListField
from ..models import Group


class GroupSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    class Meta:
        model = Group
        fields = (
            'pk',
            'interest',
            'group_img',
            'name',
            'description',
            'address',
            'lat',
            'lng',
        )


class GroupDetailSerializer(serializers.ModelSerializer):
    interest = CustomListField()
    author = SimpleUserSerializer(read_only=True)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    member = SimpleUserSerializer(many=True)
    like_users = SimpleUserSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'pk',
            'interest',
            'name',
            'group_img',
            'description',
            'address',
            'lat',
            'lng',
            'author',
            'created_date',
            'modified_date',
            'member',
            'like_users',

        )

    # 모델에 없는 필드 추가해서 보내기
    def to_representation(self, instance):
        # 기존 instance 를 받아서
        ret = super().to_representation(instance)
        # 새로 설정할 내용을 작성하고
        like_users_count = instance.get_all_like_users_count()
        member_count = instance.get_all_member_count()
        # [] 에 필드명을 지정해준다.
        ret['member_count'] = member_count
        ret['like_users_count'] = like_users_count
        return ret


class MainGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'pk',
            'lat',
            'lng',
        )
