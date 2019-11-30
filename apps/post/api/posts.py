import logging

from apps.user.models import UserProfile
from django.db.models import Case, Count, Q, When
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from tiberium.utils import get_user_profile, mark_deleted

from ..models import Like, Post, PostType
from ..serializers import PostSerializer

logger = logging.getLogger(__name__)


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostList(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = PostPagination

    def post(self, request, *args, **kwargs):
        user_profile = get_user_profile(request)
        if user_profile.is_system:
            return Response(
                'With great power comes great responsibility!', status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            )
        request.data['creator'] = user_profile.id
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        user_profile = get_user_profile(self.request)
        return Post.active.filter(Q(creator__is_system=True) | Q(creator=user_profile))


class FreshList(generics.ListAPIView):
    """
    Returns fresh posts for current user

    Posts ordered by creation time
    """

    FRESH_LIMIT = 10

    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_profile = get_user_profile(self.request)
        return Post.active.filter(Q(creator__is_system=True) | Q(creator=user_profile))[: self.FRESH_LIMIT]


class TopList(generics.ListAPIView):
    """
    Returns top posts for current user

    Posts ordered by likes cont
    """

    TOP_LIMIT = 10

    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(cache_page(5))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user_profile = get_user_profile(self.request)

        result = (
            Like.objects.values('post')
            .filter(
                Q(post__creator__is_system=True) | Q(post__creator=user_profile),
                post__is_active=True,
                creator=user_profile,
            )
            .annotate(like_count=Count('post'))
            .order_by('-like_count')
            .values('post')[: self.TOP_LIMIT]
        )

        if not result:
            return Post.active.filter(creator__is_system=True)[: self.TOP_LIMIT]

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(map(lambda x: x['post'], result))])
        return Post.active.filter(id__in=result).order_by(preserved)


class TopUserPost(generics.ListAPIView):
    """
    Collects all posts for XSS checking

    Return posts id for XSS checking
    """

    TOP_LIMIT = 10

    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        top_posts = []
        for user_profile in UserProfile.active.filter(is_system=False):
            result = (
                Like.objects.values('post')
                .filter(
                    Q(post__creator__is_system=True) | Q(post__creator=user_profile),
                    post__is_active=True,
                    post__post_type=PostType.VIDEO,
                    creator=user_profile,
                )
                .annotate(like_count=Count('post'))
                .order_by('-like_count')
                .values('post')[: self.TOP_LIMIT]
            )

            ids = [post['post'] for post in result]
            posts = Post.objects.filter(id__in=ids, creator=user_profile)
            top_posts.extend(posts)

        return top_posts


class UserPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = PostPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.active.filter(creator=user_id).order_by('-created_at')


class PostDetailed(generics.RetrieveDestroyAPIView):
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):  # pylint: disable=W0613
        return mark_deleted(self)
