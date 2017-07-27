from django.db import models
from config.settings import base
from post.models import Post


# Comment
# 	post			    Foreign(Post)
# 	author			    ForeignKey(settings.AUTH_USER_MODEL)
# 	contents		    TextField
# 	created_date		DateTimeField		        	    		auto_now_add
# 	modified_date		DateTimeField       		    			auto_now

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(base.AUTH_USER_MODEL)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
