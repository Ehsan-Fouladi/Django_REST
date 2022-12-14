from rest_framework.permissions import BasePermission
from rest_framework import permissions

class CostomPermision(BasePermission):

    def object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user