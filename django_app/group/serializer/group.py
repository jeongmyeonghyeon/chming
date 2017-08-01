from rest_framework import serializers

from ..models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'hobby',
            'author',
            'group_name',
            'group_img',
            'like_users',
            'created_date',
            'modified_date',
        )
