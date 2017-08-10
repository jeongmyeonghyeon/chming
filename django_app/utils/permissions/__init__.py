from rest_framework import permissions


class ObjectIsRequestUser(permissions.BasePermission):
    message = '접근 권한이 없습니다.'

    # 읽기 권한은 모두에게 허용하므로, GET, HEAD, OPTIONS 요청은 항상 허용함
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj == request.user


class AuthorIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
