import logging

from apps.post.tasks import like_post_after_user_create
from apps.user.models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField

logger = logging.getLogger()


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, allow_blank=False)
    login = serializers.CharField(source='username', required=True, allow_blank=False)
    name = serializers.CharField(write_only=True, required=True, allow_blank=False)
    # recaptcha = ReCaptchaField()

    class Meta:
        fields = ('login', 'password', 'name')
        # fields = ('login', 'password', 'name', 'recaptcha')

    def create(self, validated_data):
        django_serializer = DjangoUserSerializer()
        user = django_serializer.create({'username': validated_data['username']})

        user.set_password(validated_data['password'])
        user.save()

        user_profile = UserProfile()
        user_profile.login = validated_data['username']
        user_profile.name = validated_data['name']
        user_profile.user = user
        user_profile.save()
        like_post_after_user_create.delay(str(user_profile.id))
        return user

    def validate_login(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('User already exists')
        return value

    def update(self, instance, validated_data):
        pass


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True, lookup_field='username')

    class Meta:
        model = UserProfile
        fields = ('id', 'login', 'name', 'username')
