from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class FullNameSerializer(serializers.Serializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        first_name = obj.get('first_name', '')
        last_name = obj.get('last_name', '')
        if first_name and last_name:
            return f"{first_name}-{last_name}"
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        else:
            return "None"