from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User

__all__ = (
    'Logout',
)


class Logout(APIView):
    queryset = User.objects.all()

    def post(self, request, format=None):
        # simply delete the token to force a login
        return self.logout(request)

    def logout(self, request):
        try:
            print('@@@@@@@@@@', request.user)
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"detail": _("제공된 토큰이 없습니다")}, status=status.HTTP_401_UNAUTHORIZED)

        django_logout(request)

        return Response({"detail": _("Success logout")}, status=status.HTTP_200_OK)
