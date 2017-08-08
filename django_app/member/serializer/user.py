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
            'username',
            'profile_img',
            'gender',
            'birth_year',
            'birth_month',
            'birth_day',
            'hobby',
            'address',
            'lat',
            'lng',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'nickname',
            'profile_img',
            'gender',
            'birth_year',
            'birth_month',
            'birth_day',
            'hobby',
            'region',
            'joined_group',
        )


class UserCreationSerializer(serializers.Serializer):
    # Custom default error messages
    def __init__(self, *args, **kwargs):
        super(UserCreationSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['blank'] = '이 항목을 채워주세요.'
        # self.fields['email'].error_messages['invalid'] = '유효한 이메일 주소가 아닙니다.'
        self.fields['username'].error_messages['blank'] = '이 항목을 채워주세요.'

    email = serializers.EmailField(error_messages={'invalid': '유효한 이메일 주소가 아닙니다.'})
    username = serializers.CharField(max_length=100)
    profile_img = serializers.ImageField()
    password1 = serializers.CharField()
    password2 = serializers.CharField(write_only=True)
    gender = serializers.CharField(max_length=1)
    birth_year = serializers.IntegerField()
    birth_month = serializers.IntegerField()
    birth_day = serializers.IntegerField()
    hobby = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('해당 사용자 이메일은 이미 존재합니다.')
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def save(self, *args, **kwargs):
        email = self.validated_data.get('email', '')
        username = self.validated_data.get('username', '')
        profile_img = self.validated_data.get('profile_img', '')
        gender = self.validated_data.get('gender', '')
        password = self.validated_data.get('password1', '')
        birth_year = self.validated_data.get('birth_year', '')
        birth_month = self.validated_data.get('birth_month', '')
        birth_day = self.validated_data.get('birth_day', '')
        hobby = self.validated_data.get('hobby', '')
        address = self.validated_data.get('address', '')
        lat = self.validated_data.get('lat', '')
        lng = self.validated_data.get('lng', '')
        user = User.objects.create_user(
            email=email,
            username=username,
            profile_img=profile_img,
            gender=gender,
            password=password,
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            hobby=hobby,
            address=address,
            lat=lat,
            lng=lng,
        )
        return user
