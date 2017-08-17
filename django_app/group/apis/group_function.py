from rest_framework.compat import is_anonymous
from rest_framework.exceptions import APIException

from group.models import Group
from group.pagination import GroupPagination


def filtered_group_list(self):
    if not is_anonymous(self.request.user):
        origin_lat = float(self.request.GET.get('lat', self.request.user.lat))
        origin_lng = float(self.request.GET.get('lng', self.request.user.lng))
        distance_limit = float(self.request.GET.get('distance_limit', 0.5))
        hobby = self.request.GET.get('hobby', self.request.user.hobby).split(',')

        for i in range(len(hobby)):
            hobby[i] = hobby[i].strip()

        groups = Group.objects.iterator()
        filter_group_pk_list = []
        for group in groups:
            distance = group.get_distance(origin_lat, origin_lng)
            if distance < distance_limit:
                filter_group_pk_list.append(group.pk)
        if not len(filter_group_pk_list):
            raise APIException({'result': '검색결과가 없습니다.'})

        queryset = Group.objects.filter(pk__in=filter_group_pk_list).filter(hobby__in=hobby)

        if not queryset:
            raise APIException({'result': '검색결과가 없습니다.'})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return serializer

    origin_lat = float(self.request.GET.get('lat', 37.517547))
    origin_lng = float(self.request.GET.get('lng', 127.018127))
    distance_limit = float(self.request.GET.get('distance_limit', 0.5))

    if self.request.GET.get('hobby') is None:
        hobby = None
    else:
        hobby = self.request.GET.get('hobby').split(',')
        for i in range(len(hobby)):
            hobby[i] = hobby[i].strip()

    groups = Group.objects.iterator()
    filter_group_pk_list = []
    distance_dict = {}
    for group in groups:
        distance = group.get_distance(origin_lat, origin_lng)
        if distance < distance_limit:
            filter_group_pk_list.append(group.pk)

    #         distance_dict[group.pk] = distance
    # import operator
    # sorted_distance_dict = dict(sorted(distance_dict.items(), key=operator.itemgetter(1)))
    # print(sorted_distance_dict.keys())

    if not len(filter_group_pk_list):
        raise APIException({'result': '검색결과가 없습니다.'})

    if not hobby:
        queryset = Group.objects.filter(pk__in=filter_group_pk_list)
    else:
        queryset = Group.objects.filter(pk__in=filter_group_pk_list).filter(hobby__in=hobby)

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return serializer
