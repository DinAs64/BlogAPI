from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

#Permission so only the Author or the Admin can edit the post and/or comment.
class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user == obj.author or request.user.is_staff
            )
    
#Permission so only the User can edit the profile.
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

