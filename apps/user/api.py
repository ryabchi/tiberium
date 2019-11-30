from rest_framework import generics, permissions

from .models import User, UserProfile
from .serializers import UserProfileSerializer, UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileList(generics.ListAPIView):
    """
    System users profile list.

    Returns a users list for getting many UUID-s.
    """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.system_user.all()
    permission_classes = (permissions.IsAuthenticated,)


class UserProfileDetail(generics.RetrieveAPIView):
    """
    System users profile detail.

    Returns a users list for getting many UUID-s.
    """

    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return UserProfile.system_user.filter(is_system=True) | UserProfile.active.filter(user=self.request.user)
