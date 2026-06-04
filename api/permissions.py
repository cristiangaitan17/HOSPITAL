from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """Solo administradores pueden modificar, los demás solo lectura"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsMedicoOrAdmin(permissions.BasePermission):
    """Médicos y administradores tienen acceso completo"""
    
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.groups.filter(name='medicos').exists():
            return True
        return False


class IsPacienteOrAdmin(permissions.BasePermission):
    """Pacientes solo ven sus propios datos"""
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if hasattr(obj, 'paciente') and obj.paciente.user == request.user:
            return True
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if hasattr(obj, 'usuario') and obj.usuario == request.user:
            return True
        return False


class IsOwnDataOrReadOnly(permissions.BasePermission):
    """Usuarios solo pueden modificar sus propios datos"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user