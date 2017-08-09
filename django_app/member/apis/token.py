from rest_framework import parsers, renderers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from ..serializer import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializer import UserSerializer

__all__ = (
    'ObtainAuthToken',
)

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        userserializer = UserSerializer(user)
        return Response({'token': token.key, 'login_user_info': userserializer.data})



