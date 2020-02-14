from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .models import User, UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from .tasks import create_initial_users


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


class CreateInitialUsers(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        create_initial_users.delay()
        return Response('OK', status=HTTP_200_OK)
