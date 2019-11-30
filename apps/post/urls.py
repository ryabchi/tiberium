from django.conf.urls import url

from .api.likes import LikeView, PostLikeView
from .api.posts import FreshList, PostDetailed, PostList, TopList, TopUserPost, UserPostList

urlpatterns = (
    url(r'^posts$', PostList.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[0-9a-f-]{36}\Z)$', PostDetailed.as_view(), name='post-detail'),
    url(r'^posts/(?P<post_id>[0-9a-f-]+)/like$', PostLikeView.as_view(), name='post-like'),
    url(r'^posts/user/(?P<user_id>[0-9a-f-]{36}\Z)$', UserPostList.as_view(), name='user-post-list'),
    url(r'^posts/top$', TopList.as_view(), name='top'),
    url(r'^posts/fresh$', FreshList.as_view(), name='fresh'),
    url(r'^likes$', LikeView.as_view(), name='like'),
    url(r'^system/post_for_checking$', TopUserPost.as_view(), name='top-user'),
)
