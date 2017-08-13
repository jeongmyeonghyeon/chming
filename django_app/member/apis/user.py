from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import ObjectIsRequestUser
from ..serializer import UserSerializer, UserSignupUpdateSerializer
from ..models import User

__all__ = (
    'UserListView',
    'UserSignupView',
    'UserProfileView',
    'UserDeleteView',
    'IsValidEmailView',
)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupUpdateSerializer

    # Response 를 pk로 주기위해 오버라이딩
    # 여기의 create 는 CreateModelMixin 의 create 고, 걔가 save() 를 실행하면서 실행하는게 serializer 의 create 다.
    def create(self, request, *args, **kwargs):
        # 0. CreateAPIView 의 def post 의 create() 가 실행된다.
        # 1. View 의 .get_serializer 를 통해서 Serializer 의 인스턴스가 생성된다.
        # UserSignupUpdateSerializer(context={'request': < rest_framework.request.Request
        # object >, 'format': None, 'view': < member.apis.user.UserSignupView
        # object >}, data = < QueryDict: {'email': ['testuser98@ex.com'], 'password': ['1111111a'],
        #                                 'confirm_password': ['1111111a'], 'username': ['testuser98'], 'gender': ['m'],
        #                                 'birth_year': ['1986'], 'birth_month': ['8'], 'birth_day': ['4'],
        #                                 'hobby': ['football'], 'address': ['서울시 강남구 신사동'], 'lat': ['37.5215207'],
        #                                 'lng': ['127.0205784'],
        #                                 'profile_img': [ < InMemoryUploadedFile: 영화, 은교003.jpg(
        #     image / jpeg) >]} > )
        # request.data 의 데이터 타입 == <class 'django.http.request.QueryDict'>
        serializer = self.get_serializer(data=request.data)
        # 2. is_valid 가 True 면,
        serializer.is_valid(raise_exception=True)
        # View에 있는 .create() 와 UserCreation... .create() 는 연결되있다.
        # 유효성이 검사 된 데이터를 기반으로 객체 인스턴스를 반환 할 수 있습니다.
        # 3. instace.save() 로 UserSignupUpdateSerializer 의 .create() 로 들어감(data=data 이므로...) 짜란~
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        # Response를 위한 pk값
        pk = User.objects.get(email=serializer.data['email']).pk
        return Response({"pk": pk}, status=status.HTTP_201_CREATED, headers=headers)


class UserProfileView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        instance = Token.objects.get(key=request._auth).user
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = UserSignupUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"pk": instance.pk})


class UserDeleteView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def delete(self, request):
        user = request.user
        user.delete()
        ret = {
            "detail": "유저가 삭제되었습니다."
        }
        return Response(ret)


class IsValidEmailView(APIView):
    def get(self, request):
        if User.objects.filter(email=request.GET['email']).exists():
            ret = {'is_valid': False}
        else:
            ret = {'is_valid': True}
        return Response(ret)
