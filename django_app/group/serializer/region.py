from rest_framework import serializers

from group.models import Region


class RegionSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    class Meta:
        model = Region
        fields = (
            'pk',
            'level1',
            'level2',
            'level3',
            'lat',
            'lng',
        )
