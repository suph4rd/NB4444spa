from rest_framework.permissions import BasePermission


class IsSuperUserOrOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(
            request.user.is_authenticated
            and (
                request.user.is_superuser or
                request.user == obj.user
            )
        )
