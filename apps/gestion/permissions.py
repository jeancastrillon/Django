from rest_framework.permissions import BasePermission, IsAuthenticated

class IsStaffUser(BasePermission):
    """
    Permite acceso solo a usuarios autenticados y con is_staff = True
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )