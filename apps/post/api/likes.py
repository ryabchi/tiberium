import json

import coreapi
from rest_framework import generics, permissions, status
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from tiberium.utils import get_user_profile, is_uuid

from ..models import Like, Post
from ..serializers import LikeSerializer


class SimpleFilterBackend(BaseFilterBackend):  # pylint: disable=W0223
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='post_ids', location='query', required=False, type='string', description='Posts UUID list'
            )
        ]


class LikeView(generics.ListCreateAPIView):
    filter_backends = (SimpleFilterBackend,)

    LIKE_PARAM = 'post_ids'
    DIVIDER = ','
    MAX_POSTS_COUNT = 10

    model = Like
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create_error_message(self, message):
        error_message = json.dumps({self.LIKE_PARAM: [message]})
        return Response(error_message, status=HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        raw_posts = self.request.GET.get(self.LIKE_PARAM)
        if not raw_posts:
            return self.create_error_message('This field is required.')

        posts = raw_posts.split(self.DIVIDER)
        if len(posts) > self.MAX_POSTS_COUNT:
            return self.create_error_message('Wow. Wow. Too much posts.')

        for post_uuid in posts:
            if not is_uuid(post_uuid):
                return self.create_error_message("It's not UUID. Don't try to hack us. ^_^")

        user_profile = get_user_profile(self.request)

        post_list = Post.active.filter(id__in=posts)
        return Response({str(post.id): post.get_like(user_profile) for post in post_list}, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not is_uuid(request.data['userId']):
            return Response('Invalid user', status=status.HTTP_400_BAD_REQUEST)
        user_profile = get_user_profile(request)
        if user_profile.is_system:
            return Response(
                'Well, if computers could think, there’d be none of us here, would there?',
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )
        request.data['creator'] = user_profile.id
        liked = Like.objects.filter(
            creator=request.data['creator'], user_id=request.data['userId'], post=request.data['post']
        ).first()
        if liked:
            liked.delete()
            return Response(status=HTTP_200_OK)
        return self.create(request, *args, **kwargs)


class PostLikeView(APIView):
    def get(self, _, post_id):
        if not is_uuid(post_id):
            error_message = json.dumps({'error': f"It's not uuid {post_id}"})
            return Response(error_message, status=HTTP_400_BAD_REQUEST)
        like_count = Like.objects.filter(creator=get_user_profile(self.request), post_id__id=post_id).count()
        return Response(json.dumps({post_id: like_count}), status=HTTP_200_OK)
