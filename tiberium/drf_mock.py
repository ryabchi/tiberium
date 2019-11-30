from datetime import datetime

from apps.user.models import UserProfile
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    username = get_username(user)
    profile = UserProfile.active.filter(user=user).first()
    if profile:
        user_id = str(profile.id)
    else:
        user_id = None
    # 'user_id': user.pk,  # comment. may be use uuid?
    payload = {'username': username, 'user_id': user_id, 'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA}

    return payload
