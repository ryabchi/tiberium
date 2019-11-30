import uuid

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    Index,
    Manager,
    Model,
    OneToOneField,
    TextField,
    UUIDField,
)
from tiberium.query_manager import ActiveObjectManager, SystemUserObjectManager


class UserRole:
    USUAL = 'U'
    ADMIN = 'A'

    CHOICES = ((USUAL, 'user'), (ADMIN, 'admin'))


class UserProfile(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile')
    role = CharField(max_length=1, choices=UserRole.CHOICES, default=UserRole.USUAL)
    is_system = BooleanField(default=False)
    login = CharField(null=False, unique=True, max_length=255)
    name = CharField(null=False, max_length=255)
    updated_at = DateTimeField(auto_now=True, editable=False)
    created_at = DateTimeField(auto_now_add=True, editable=False)
    is_active = BooleanField(default=True)

    objects = Manager()
    active = ActiveObjectManager()
    system_user = SystemUserObjectManager()

    class Meta:
        verbose_name = "User Profile"
        ordering = ('pk',)

        indexes = [Index(fields=['is_system'])]

    def __str__(self):
        return self.login

    @staticmethod
    def get_profile_by_user(user):
        return UserProfile.objects.filter(user=user.id).first()


class SystemUserData(Model):
    profile = OneToOneField(UserProfile, on_delete=CASCADE, related_name='system_user_data', null=False)
    password = TextField(null=True, blank=True)

    objects = Manager()

    def __str__(self):
        return self.profile.login  # pylint: disable=E1101
