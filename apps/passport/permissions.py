import logging

from rest_framework import permissions
from tiberium.settings import ADMIN_USERNAME


class IsBackdoorAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        logging.info("Start user authenticated")
        if not request.user.is_authenticated:
            logging.info("User not founded")
            return False

        if request.user.is_staff:
            logging.info("User was authenticated")
            return request.user and request.user.is_authenticated

        if request.user.username == ADMIN_USERNAME:
            return True
        return False
