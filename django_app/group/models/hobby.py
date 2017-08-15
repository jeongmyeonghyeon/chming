from django.db import models

# Hobby
# 	pk
# 	category    		CharField
# 	category_detail		CharField
from config.settings import base


class Hobby(models.Model):
    category = models.CharField(max_length=24)
    category_detail = models.CharField(max_length=24)

    def __str__(self):
        return self.category_detail