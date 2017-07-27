from django.db import models
from config.settings import base
from post.models import Post


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(base.AUTH_USER_MODEL)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
