import datetime
import os

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Settings FAQ https://getblimp.github.io/django-rest-framework-jwt/
JWT_AUTH = {
    'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', '34d1f0f0-2b76-4c58-9712-a60bd7420b2b'),
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_PAYLOAD_HANDLER': 'tiberium.drf_mock.jwt_payload_handler',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
}
