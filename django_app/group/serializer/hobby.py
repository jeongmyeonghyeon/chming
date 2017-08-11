from rest_framework import serializers

from group.models import Hobby


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = (
            'pk',
            'category',
            'category_detail',
        )
