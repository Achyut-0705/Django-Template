from rest_framework import permissions

class isOfficer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and (request.user.role == "SuperAdmin" or request.user.role == "Admin"):
            return True
        return False
