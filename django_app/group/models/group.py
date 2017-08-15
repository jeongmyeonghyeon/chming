from django.db import models

from config.settings import base
from utils.fields import CustomImageField
from utils.group import distance_calculator
from math import sin, cos, sqrt, atan2, radians


# Group
# 	pk
# 	hobby			    CharField
# 	author			    ForeignKey(settings.AUTH_USER_MODEL)
# 	group_name		    CharField					            max_length=255
# 	group_img		    CustomImageField				        upload_to=group, blank=true
# 	like_users		    ManyToMany(GroupLike)
# 	created_date		DateTimeField			    	    	auto_now_add
# 	modified_date		DateTimeField				    	    auto_now
# 	(terminated_date	삭제기능구현)
# 	lat
# 	lng

# GroupLike
# 	group			    ForeignKey(Group)
# 	user			    ForeignKey(settings.AUTH_USER_MODEL)
# 	created_date		DateTimeField	        				auto_now_add


class Group(models.Model):
    hobby = models.CharField(max_length=100)
    author = models.ForeignKey(
        base.AUTH_USER_MODEL,
        related_name='open_groups'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = CustomImageField(
        upload_to='group/%Y/%m/%d',
        blank=True,
    )
    like_users = models.ManyToManyField(
        base.AUTH_USER_MODEL,
        through='GroupLike',
        related_name='like_groups',
    )
    address = models.CharField(max_length=100, default='')
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(
        base.AUTH_USER_MODEL,
        related_name='joined_groups',
    )

    def __str__(self):
        return self.name

    def get_all_member(self):
        return self.members.all()

    def get_all_member_count(self):
        return self.members.count()

    def get_all_like_users(self):
        return self.like_users.all()

    def get_all_like_users_count(self):
        return self.like_users.count()


    def get_distance(self, origin_lat, origin_lng):
        target_lat = self.lat
        target_lng = self.lng
        # return distance_calculator(origin_lat, origin_lng, target_lat, target_lng)
        R = 6373.0

        origin_lat = radians(origin_lat)
        origin_lng = radians(origin_lng)
        target_lat = radians(target_lat)
        target_lng = radians(target_lng)

        dlon = target_lng - origin_lng
        dlat = target_lat - origin_lat

        a = sin(dlat / 2) ** 2 + cos(origin_lat) * cos(target_lat) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        # 1 = 1 km
        # 0.5 = 5,00 m
        return distance


class GroupLike(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(base.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('group', 'user'),
        )

    def __str__(self):
        return '{}|{}'.format(self.group.name, self.user.username)
