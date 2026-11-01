from rest_framework.permissions import BasePermission


class EsAdministrador(BasePermission):
    """Permite el acceso exclusivo a usuarios con rol de administrador."""
    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        return bool(request.user and request.user.is_authenticated and request.user.rol == 'administrador')