from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from group.models import Group, Hobby
from utils.fields import CustomListField
from ..models import User

__all__ = (
    'UserSerializer',
    'UserSignupSerializer',
    'UserUpdateSerializer',
)


class GroupSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

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


# pk, category, category_detail, name, image

class UserPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
        )


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'profile_img',
            'username',
        )


class UserSerializer(serializers.ModelSerializer):
    hobby = CustomListField()
    open_groups = GroupSerializer(read_only=True, many=True)
    joined_groups = GroupSerializer(read_only=True, many=True)
    like_groups = GroupSerializer(read_only=True, many=True)

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
            'open_groups',
            'joined_groups',
            'like_groups',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    class Meta:
        model = User
        fields = fields = (
            'pk',
            'email',
            'username',
            'password',
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

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        # info = model_meta.get_field_info(instance)

        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            # # 다대다 관계에 대한 어떤 처리를 다룬 것 같다.
            # # 그게 구체적으로 어떤 처리인지 모르겠다. (아마 다대다 관계의 인스턴스의 필드를 불러와 그 부분까지 수정해주는 정도로 이해된다.
            # # 주석처리해도 작동한다.
            # # 관계에 대한 검사를 하지 않으므로, instnace의 정보를 가져오는 info 인스턴스 역시 사용할 필요가 없어졌다.
            # if attr in info.relations and info.relations[attr].to_many:
            #     set_many(instance, attr, value)
            # else:

            # setattr(x, 'y', v) is equivalent to ``x.y = v''
            setattr(instance, attr, value)
        instance.set_password(password)
        instance.save()

        return instance


class UserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    # profile_img = serializers.ImageField()

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'username',
            'password',
            'confirm_password',
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

    def validate(self, data):
        """
        Checks to be sure that the received password and confirm_password
        fields are exactly the same
        """
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        if not 'profile_img' in data:
            data['profile_img'] = 'images/profile.png'
        return data

    def create(self, validated_data):
        """
        Creates the user if validation succeeds
        """
        # is_valid() 를 통해 생성된 validated_data 에서 set_password 를 위한 password 만 pop으로 추출
        password = validated_data.pop('password', None)
        # password를 제외한 user instance 생성
        # User({'email': 'testuser91@ex.com', 'username': 'testuser91', 'profile_img': <InMemoryUploadedFile: 영화,은교003.jpg (image/jpeg)>, 'gender': 'm', 'birth_year': 1986, 'birth_month': 8, 'birth_day': 4, 'hobby': 'football', 'add': '서울시 강남구 신사동', 'lat': 37.5215207, 'lng': 127.0205784})
        user = self.Meta.model(**validated_data)
        # set_password 를 통해 비밀번호 해시
        user.set_password(password)
        # 데이터베이스에 저장
        # return user 를 주석처리해도 데이터베이스에는 유저가 추가됨...
        user.save()
        return user
