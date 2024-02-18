from djoser.serializers import UserSerializer
from rest_framework import serializers

from tasks.models import Task, User


class CustomUserSerializer(UserSerializer):
    """Serialization for users."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class TaskSerializer(serializers.ModelSerializer):
    """Serialization for tasks."""

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'user_id')
        read_only_fields = ('user_id',)
