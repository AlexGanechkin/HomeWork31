from rest_framework.permissions import BasePermission

from ads.models import UserRoles


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            owner = obj.owner
        elif hasattr(obj, "author_id"):
            owner = obj.author_id
        else:
            return False

        if request.user == owner:
            return True

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True
