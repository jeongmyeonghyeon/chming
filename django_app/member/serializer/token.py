from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

__all__ = (
    'AuthTokenSerializer',
)


class AuthTokenSerializer(serializers.Serializer):
    # Custom default error messages
    def __init__(self, *args, **kwargs):
        super(AuthTokenSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['blank'] = '이 항목을 채워주세요.'
        self.fields['password'].error_messages['blank'] = '이 항목을 채워주세요.'

    email = serializers.EmailField()
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('제공된 credentials로 로그인 할 수 없습니다.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
