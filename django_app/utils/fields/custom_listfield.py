from rest_framework import serializers


class CustomListField(serializers.ListField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        split_hobby = data.split(',')
        for i in range(len(split_hobby)):
            split_hobby[i] = split_hobby[i].strip()
        # return [self.child.to_representation(item) if item is not None else None for item in data]
        return split_hobby
