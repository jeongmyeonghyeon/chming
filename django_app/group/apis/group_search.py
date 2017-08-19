import operator
from functools import reduce

from django.db.models import Q

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from group.models import Group
from group.serializer.group import GroupListSerializer


class GroupSearchView(APIView):
    def get(self, request, *args, **kwargs):
        search = self.request.GET.get("search")

        if search is None or search == " ":
            raise APIException({'result': '검색어를 입력해주세요.'})

        search = self.request.GET.get("search").split()
        search_type = self.request.GET.get("search_type", "all")

        if search_type == "hobby":
            queryset = Group.objects.filter(hobby__in=search)
        elif search_type == "group":
            queryset = Group.objects.filter(reduce(operator.or_, (Q(name__contains=x) for x in search)) |
                                            reduce(operator.or_, (Q(description__contains=x) for x in search))
                                            )
        elif search_type == "address":
            queryset = Group.objects.filter(reduce(operator.or_, (Q(address__contains=x) for x in search)))
        else:
            queryset = Group.objects.filter(
                reduce(operator.or_, (Q(hobby__contains=x) for x in search)) |
                reduce(operator.or_, (Q(name__contains=x) for x in search)) |
                reduce(operator.or_, (Q(description__contains=x) for x in search)) |
                reduce(operator.or_, (Q(address__contains=x) for x in search))
            )

        if not queryset.exists():
            raise APIException({'result': '검색결과가 없습니다.'})

        serializer = GroupListSerializer(queryset, many=True)
        return Response(serializer.data)
