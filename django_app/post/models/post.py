from django.db import models
from config.settings import base


# Post
# 	pk
# 	title			CharField					max_length=100
# 	content			TextField
# 	group			Foreign(Group)
# 	author			ForeignKey(settings.AUTH_USER_MODEL)
# 	img			    ImageField					upload_to=post, blank=true
# 	post_type
# 	created_date
# 	modified_date

# PostLike
# 	post			ForeignKey(Group)
# 	user			ForeignKey(settings.AUTH_USER_MODEL)
# 	created_date		DateTimeField					auto_now_add

class Post(models.Model):
    post_type = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    group = models.ForeignKey('group.Group')
    author = models.ForeignKey(base.AUTH_USER_MODEL)
    img = models.ImageField(
        upload_to='post/%Y/%m/%d',
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_d_date = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(base.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('post', 'user'),
        )
