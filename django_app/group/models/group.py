from django.db import models

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

from config.settings import base
from utils.fields import CustomImageField


class Group(models.Model):
    hobby = models.CharField(max_length=100)
    author = models.ForeignKey(base.AUTH_USER_MODEL)
    group_name = models.CharField(max_length=100)
    group_img = CustomImageField(
        upload_to='group/%Y/%m/%d',
        blank=True,
    )
    like_users = models.ManyToManyField(
        base.AUTH_USER_MODEL,
        through='GroupLike',
        related_name='like_groups',
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.group_name


class GroupLike(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(base.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('group', 'user'),
        )
