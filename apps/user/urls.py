from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import api

urlpatterns = (
    url(r'^userprofiles/register$', api.UserCreate.as_view(), name='user-create'),
    url(r'^userprofiles$', api.UserProfileList.as_view(), name='userprofile-list'),
    url(r'^userprofiles/(?P<pk>[0-9a-f-]{36}\Z)$', api.UserProfileDetail.as_view(), name='userprofile-detail'),
    url(r'^system/create_initial_users$', api.CreateInitialUsers.as_view(), name='create-initial-users'),
)

urlpatterns += (url(r'^jwt-token-auth/', obtain_jwt_token, name='jwt-auth'),)
