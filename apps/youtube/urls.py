from django.conf.urls import url

from . import api

urlpatterns = (url(r'^youtube/tokens$', api.YoutubeTokenView.as_view(), name='get-youtube-token'),)
