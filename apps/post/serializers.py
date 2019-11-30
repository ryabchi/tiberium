import logging

from apps.user.serializers import UserProfileSerializer
from rest_framework import serializers
from tiberium.utils import get_user_profile

from .models import Like, Post

logger = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    creator_info = UserProfileSerializer(source='creator', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'post_type', 'text', 'youtube_link', 'creator', 'creator_info', 'created_at')
        read_only_fields = ('creator_info', 'created_at')


class LikeSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user_id')

    class Meta:
        model = Like
        fields = ('userId', 'post')

    def create(self, validated_data):
        validated_data['creator'] = get_user_profile(self.context.get("request"))
        like = Like.objects.create(**validated_data)
        return like

    def update(self, instance, validated_data):
        pass
