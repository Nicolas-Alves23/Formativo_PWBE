from rest_framework.permissions import BasePermission


class IsGestor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == "G"


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == "P"


class IsGestorOuDono(BasePermission):
    def has_object_permission(self, request, view, obj):
       if request.user.tipo == 'G':
           return True
       return obj.professor == request.user