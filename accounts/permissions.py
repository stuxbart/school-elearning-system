from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_teacher)


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return True


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            return bool(request.user == obj.owner)
        else:
            return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdminStaffCurrentUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_admin or user.is_staff or user == obj)


class IsAdminStaffDeleteOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return bool(request.user.is_admin or request.user.is_staff)
        return True


class IsAdminStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_admin or request.user.is_staff)


class IsAdminStaffTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_admin or user.is_staff or user.is_teacher)


class IsAdminStaffOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_admin or user.is_staff or user == obj.owner)
