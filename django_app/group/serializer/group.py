from rest_framework import serializers

from member.serializer import UserSerializer
from ..models import Group


class GroupSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

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

