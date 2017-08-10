from rest_framework import serializers

from member.serializer import UserSerializer
from ..models import Group


class GroupSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    class Meta:
        model = Group
        fields = (
            'pk',
            'hobby',
            'author',
            'group_name',
            'group_img',
            'like_users',
            'created_date',
            'modified_date',
            'lat',
            'lng',
        )


class MainGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'pk',
            'lat',
            'lng',
        )
