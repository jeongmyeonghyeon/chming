from django.db import models


# Hobby
# 	pk
# 	category    		CharField
# 	category_detail		CharField

class Hobby(models.Model):
    category = models.CharField(max_length=24)
    category_detail = models.CharField(max_length=24)
