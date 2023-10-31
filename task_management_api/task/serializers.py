from rest_framework import serializers
from .models import Task, TaskList, Attachment
from house.models import House

class TaskListSerializer(serializers.ModelSerializer):

    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), many=False, view_name='house-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    tasks = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='task-detail')

    class Meta:
        model = TaskList
        fields = ['url', 'id', 'name', 'description', 'status', 'created_at', 'created_by', 'house', 'tasks']
        read_only_fields = ['created_at', 'status']

    
class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name='tasklist-detail')
    attachments = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='attachment-detail')

    def validate_task_list(self, value):
        user_profile = self.context['request'].user.profile
        if value not in user_profile.house.lists.all():
            raise serializers.ValidationError('task:House not related to user')
        return value
    
    def create(self, validate_data):
        user_profile = self.context['request'].user.profile
        task = Task.objects.create(**validate_data)
        task.created_by = user_profile
        task.save()
        return task

    class Meta:
        model = Task
        fields = ['url', 'id', 'name', 'description', 'status', 'created_at', 'completed_at', 'created_by'
                  , 'completed_by', 'task_list', 'attachments']
        read_only_fields = ['created_at', 'created_by', 'completed_at', 'completed_by', 'status']


class AttachmentSerializer(serializers.ModelSerializer):

    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name='task-detail')

    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        task = attrs['task']
        task_list = TaskList.objects.get(tasks__id__exact=task.id)
        if task_list not in user_profile.house.lists.all():
            raise serializers.ValidationError('task:House not related to user')
        return attrs
    class Meta:
        model = Attachment
        fields = ['url', 'id', 'created_at', 'data', 'task']
        read_only_fields = ['created_at']
