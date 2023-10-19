from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    class Meta:
        model = House
        fields = ['url', 'name', 'image', 'created_at', 'description', 'manager', 'points',
                  'completed_task_count', 'incompleted_task_count', 'members_count', 'members']
        
        read_only_fields = ['points', 'completed_task_count', 'incompleted_task_count']