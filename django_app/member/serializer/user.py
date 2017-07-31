from curses.ascii import isdigit

from django.core.validators import MaxValueValidator
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


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'password1',
            'password2',
            'nickname',
            'profile_img',
            'birth_year',
            'birth_month',
            'birth_day',
            'hobby',
            'region',
        )


class UserCreationSerializer(serializers.Serializer):
    username = serializers.EmailField()
    nickname = serializers.CharField(
        max_length=100,
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    birth_year = serializers.IntegerField()
    birth_month = serializers.IntegerField()
    birth_day = serializers.IntegerField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exist')
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords didn\'t match')
        return data

    def save(self, *args, **kwargs):
        email = self.validated_data.get('username', '')
        nickname = self.validated_data.get('nickname', '')
        password = self.validated_data.get('password1', '')
        birth_year = self.validated_data.get('birth_year', '')
        birth_month = self.validated_data.get('birth_month', '')
        birth_day = self.validated_data.get('birth_day', '')
        user = User.objects.create_user(
            username=email,
            nickname=nickname,
            password=password,
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
        )
        return user
