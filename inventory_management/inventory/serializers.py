from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
    
    def validate_created_at(self, value):
        if value is not None and not isinstance(value, str):
            raise serializers.ValidationError("created_at must be a string in ISO 8601 format.")
        return value
