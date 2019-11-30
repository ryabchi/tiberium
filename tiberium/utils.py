import random
from uuid import UUID

from apps.user.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.response import Response


def mark_deleted(self):
    obj = self.get_object()

    obj.is_active = False
    try:
        obj.save()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_204_NO_CONTENT)


def is_uuid(data):
    try:
        UUID(data, version=4)
    except ValueError:
        return False

    return True


def get_user_profile(request):
    user = None
    if request and hasattr(request, 'user'):
        user = UserProfile.get_profile_by_user(request.user)
    if not user:
        raise serializers.ValidationError("User doesn't exists")
    return user


def yes_or_no():
    return bool(random.getrandbits(1))
