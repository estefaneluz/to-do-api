from rest_framework import serializers
from .models import TaskItem, Tag
from users.models import User

class TagSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = ['id', 'name', 'hex_color', 'created_by']

    def get_created_by(self, obj):
        return obj.created_by.name

class TaskItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = TaskItem
        fields = ['id', 'title', 'status', 'tags', 'created_by', 'is_active', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']

    def get_created_by(self, obj):
        return obj.created_by.name