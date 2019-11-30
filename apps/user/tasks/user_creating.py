# pylint: disable=no-member
import random

from apps.passport.models import Passport
from apps.post.models import Post, PostType
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from faker import Faker
from tiberium.celery import app
from tiberium.utils import yes_or_no

from ..models import SystemUserData, UserProfile

PASSWORD_LENGTH = 30
fake = Faker()

VIDEO_LIST = [
    'XAwqoFzK2wM',
    'jj9FnEOwh1I',
    'RWksplaFQGk',
    'U4W9j1fpst4',
    '0aVlqo0rUCg',
    '2xS6I8DSDcA',
    'JyElnperhwk',
    'BT5IkJXfd14',
    'YL3RafApIxo',
    'kGYIQfqmHIg',
    '_s6WgXIpX68',
    'BoGB9d-Vvto',
    'DCTJNujRRfg',
    'DT-fkdtHY2o',
    'qpWrK87wKUA',
    '-HkyiRNGyDs',
    'OSH3bS3Xr0s',
    'AWgsLLfr8-4',
    'WKvocPF1-PU',
    '6poctdEpbSI',
    'rscsSVl3AFA',
    '-1GBxwzQiQ8',
    'VfjQHkV2kY0',
    'oD2-A7ukRGQ',
    'vGw5oe7wqfI',
    'T9DYQvpm8KI',
    'e-EQ_GGj-qQ',
    'tQhOjd0018s',
    'CVIEgX6V_RY',
    'I9VZuo_VAP4',
]


def create_system_user():
    password = BaseUserManager().make_random_password(PASSWORD_LENGTH)
    user = User()
    user.username = fake.user_name()
    user.set_password(password)
    user.save()

    user_profile = UserProfile.objects.create(user=user, is_system=True, login=user.username, name=fake.name())

    SystemUserData.objects.create(profile=user_profile, password=password)
    return user_profile


@app.task()
def create_system_user_task():
    return create_system_user()


@app.task()
def create_initial_users():
    random.seed()

    videos = VIDEO_LIST.copy()

    user_posts = []
    user_passports = []

    for _ in range(settings.INITIAL_USER_COUNT):
        user_profile = create_system_user()
        user_posts.extend(get_user_posts(user_profile, videos))
        user_passports.extend(create_passport(user_profile))

    random.shuffle(user_posts)
    Post.objects.bulk_create(user_posts)
    Passport.objects.bulk_create(user_passports)


def get_user_posts(user_profile, videos):
    posts = []
    for _ in range(random.randint(5, 10)):
        if videos and yes_or_no() and yes_or_no():
            posts.append(Post(post_type=PostType.VIDEO, youtube_link=videos.pop(), creator=user_profile))
            continue
        posts.append(Post(post_type=PostType.TEXT, text=fake.text(), creator=user_profile))
    return posts


def create_passport(user_profile):
    passports = []
    # passport
    if yes_or_no():
        passports.append(Passport(name='passport', secret=fake.itin(), creator=user_profile))
    # driver licence
    if yes_or_no():
        passports.append(Passport(name='driver licence', secret=fake.ein(), creator=user_profile))
    return passports
