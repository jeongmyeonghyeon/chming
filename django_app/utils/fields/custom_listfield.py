from rest_framework import serializers


class CustomListField(serializers.ListField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        split_interest = data.split(',')
        for i in range(len(split_interest)):
            split_interest[i] = split_interest[i].strip()
        # return [self.child.to_representation(item) if item is not None else None for item in data]
        return split_interest
