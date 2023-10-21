from rest_framework import permissions

class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    '''Custom permission for TaskListViewSets to only allow the creator editing permission.'''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user.profile == obj.created_by