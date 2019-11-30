from django.conf.urls import url

from .api import PassportBackdoor, PassportDetail, PassportList

urlpatterns = (
    url(
        r'^passports/backdoor/users/(?P<user_id>[0-9a-f-]{36}\Z)$',
        PassportBackdoor.as_view(),
        name='passport-backdoor-list',
    ),
    url(r'^passports$', PassportList.as_view(), name='passport-list'),
    url(r'^passports/(?P<pk>[0-9a-f-]{36}\Z)$', PassportDetail.as_view(), name='passport-detail'),
)
