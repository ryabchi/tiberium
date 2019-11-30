'''tiberium URL Configuration'''
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Tiberium API',
        default_version='v1',
        description='CTF Tiberium API',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='cyberxx@yandex.ru'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(f'api/{settings.ADMIN_URL}/', admin.site.urls),
    path('api/v1/', include('apps.user.urls')),
    path('api/v1/', include('apps.post.urls')),
    path('api/v1/', include('apps.passport.urls')),
    path('api/v1/', include('apps.youtube.urls')),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += [
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
