from rest_framework.permissions import BasePermission


class IsSuperUserOrOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        owner = obj.plan.user if hasattr(obj, 'plan') else obj.user
        return request.user.is_superuser or request.user == owner
