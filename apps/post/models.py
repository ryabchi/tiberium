import uuid

from apps.user.models import UserProfile
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    Index,
    Manager,
    Model,
    TextField,
    UUIDField,
)
from tiberium.query_manager import ActiveObjectManager


class PostType:
    TEXT = 'text'
    VIDEO = 'video'
    IMAGE = 'image'

    CHOICES = ((TEXT, 'text'), (VIDEO, 'video'), (IMAGE, 'image'))


class Post(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    post_type = CharField(max_length=10, choices=PostType.CHOICES, default=PostType.TEXT)
    text = TextField(default='', null=True, blank=True)
    youtube_link = TextField(null=True, blank=True)
    image = ImageField(upload_to='photos', max_length=254, null=True)
    creator = ForeignKey(UserProfile, on_delete=CASCADE, related_name='created_by')
    created_at = DateTimeField(auto_now_add=True, editable=False)
    is_active = BooleanField(default=True)

    objects = Manager()
    active = ActiveObjectManager()

    class Meta:
        verbose_name = 'Wall Post'
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.id)

    def get_like(self, user_profile):
        is_liked_by_user = Like.objects.filter(creator=user_profile, user_id=user_profile.id, post=self.id).exists()
        count = Like.objects.filter(creator=user_profile, post=self.id).count()
        return {'liked_by_user': is_liked_by_user, 'count': count}


class Like(Model):
    user_id = UUIDField(max_length=255, null=False)
    post = ForeignKey(Post, on_delete=CASCADE, related_name='likes_counter')
    creator = ForeignKey(UserProfile, on_delete=CASCADE)

    objects = Manager()

    class Meta:
        indexes = [Index(fields=['post', 'creator'])]

    def __str__(self):
        return f'{self.creator}:{self.user_id}:{self.post}'
