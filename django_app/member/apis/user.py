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
    'UserUpdateView',
    'UserRetrieveDestroyView',
    'UserProfileView',
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
        serializer = self.get_serializer(data=request.data)
        # 2. is_valid 가 True 면,
        serializer.is_valid(raise_exception=True)
        # View에 있는 .create() 와 UserCreation... .create() 는 연결되있다.
        # 유효성이 검사 된 데이터를 기반으로 객체 인스턴스를 반환 할 수 있습니다.
        # 3. instace.save() 로 UserSignupUpdateSerializer 의 .create() 로 들어감(data=data 이므로...) 짜란~
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Response를 위한 pk값
        pk = User.objects.get(email=serializer.data['email']).pk
        return Response({"pk": pk}, status=status.HTTP_201_CREATED, headers=headers)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupUpdateSerializer

    permission_classes = (
        permissions.IsAuthenticated,
        ObjectIsRequestUser,
    )

    # Response 를 pk로 주기위해 오버라이딩
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            # 'prefetch_related'가 쿼리 세트에 적용된 경우 인스턴스의 프리 페치 캐시를 강제로 무효화해야합니다.
            instance._prefetched_objects_cache = {}
        pk = User.objects.get(email=serializer.data['email']).pk
        return Response({"pk": pk})


class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        ObjectIsRequestUser,
    )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "유저가 삭제되었습니다."})


class UserProfileView(APIView):
    def get(self, request):
        instance = Token.objects.get(key=request._auth).user
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    permission_classes = (
        permissions.IsAuthenticated,
    )
