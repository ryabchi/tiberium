import uuid

from apps.user.models import UserProfile
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    TextField,
    UUIDField,
)
from tiberium.query_manager import ActiveObjectManager


class Passport(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = CharField(max_length=250, null=False)
    secret = TextField(null=False)
    creator = ForeignKey(UserProfile, on_delete=CASCADE, related_name='passport_created_by', null=False)
    created_at = DateTimeField(auto_now_add=True, editable=False)
    is_active = BooleanField(default=True)

    objects = Manager()
    active = ActiveObjectManager()

    class Meta:
        verbose_name = "Passport"
        ordering = ('pk',)

    def __str__(self):
        return f'{self.id}:{self.creator}'
