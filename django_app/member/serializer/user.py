from rest_framework import serializers

from ..models import User

__all__ = (
    'UserSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'nickname',
            'profile_img',
            'birth_year',
            'birth_month',
            'birth_day',
            'hobby',
            'region',
            'joined_group',
        )
