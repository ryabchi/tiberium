# pylint: disable=no-member
import random
import uuid

from apps.passport.models import Passport
from apps.post.models import Like, Post, PostType
from apps.user.models import UserProfile
from apps.user.tasks.user_creating import create_passport, create_system_user
from faker import Faker
from tiberium.celery import app
from tiberium.utils import yes_or_no

PASSWORD_LENGTH = 12
fake = Faker()


@app.task()
def run_social_life():
    random.seed()

    create_new_user = yes_or_no()
    if create_new_user:
        user_profile = create_system_user()
        Post.objects.create(post_type=PostType.TEXT, text=fake.text(), creator=user_profile)
        passports = create_passport(user_profile)
        Passport.objects.bulk_create(passports)

    system_users = UserProfile.active.filter(is_system=True)

    if not system_users:
        raise Exception('Users not founded')

    create_posts(system_users)
    create_likes()


def create_posts(system_users):
    new_posts = []
    for _ in range(2):
        user_profile = system_users[random.randint(0, system_users.count() - 1)]
        new_posts.append(Post(post_type=PostType.TEXT, text=fake.text(), creator=user_profile))
    Post.objects.bulk_create(new_posts)


def create_likes():
    likes = []
    posts = Post.active.filter(creator__is_system=True)

    for user_profile in UserProfile.active.filter(is_system=False):
        for post in posts:
            likes.extend(do_like(post, user_profile))

    Like.objects.bulk_create(likes)


def do_like(post, user_profile):
    if random.choice([True, False, False, False]):
        return [Like(user_id=uuid.uuid4(), post=post, creator=user_profile)]
    return []
