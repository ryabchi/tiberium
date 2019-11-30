# pylint: disable=no-member
from apps.post.models import Post, PostType
from faker import Faker

fake = Faker()


def create_post_for_user(user_profile, post_type=PostType.TEXT):
    if post_type == PostType.TEXT:
        Post.objects.create(post_type=PostType.TEXT, text=fake.text(), creator=user_profile)
    else:
        Post.objects.create(post_type=PostType.VIDEO, youtube_link=fake.text(), creator=user_profile)
