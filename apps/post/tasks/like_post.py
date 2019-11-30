import random
import uuid

from apps.post.models import Like, Post
from apps.user.models import UserProfile
from django.conf import settings
from tiberium.celery import app


@app.task()
def like_post_after_user_create(user_profile_id):
    user_profile = UserProfile.active.filter(id=user_profile_id).first()
    if not user_profile:
        raise Exception(f'User profile {user_profile_id} not found')
    posts = Post.active.filter(creator__is_system=True)
    random.seed()

    users_like = []

    for post in posts:
        for _ in range(random.randint(10, settings.MAX_INITIAL_LIKES_ON_POST)):
            users_like.append(Like(user_id=uuid.uuid4(), post=post, creator=user_profile))

    Like.objects.bulk_create(users_like)
