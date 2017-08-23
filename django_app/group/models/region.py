from django.db import models


# Region
# 	pk
# 	si			CharField					max_length=20
# 	gu			CharField					max_length=20
# 	dong		CharField					max_length=20
# 	lat			FloatField
# 	lng			FloatField

class Region(models.Model):
    level1 = models.CharField(max_length=24, blank=True)
    level2 = models.CharField(max_length=24, blank=True)
    level3 = models.CharField(max_length=24, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return '{} {} {}'.format(self.level1, self.level2, self.level3)
