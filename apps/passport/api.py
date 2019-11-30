from rest_framework import generics, permissions
from tiberium.utils import get_user_profile, mark_deleted

from .models import Passport
from .permissions import IsBackdoorAuthenticated
from .serializers import PassportSerializer


class PassportList(generics.ListCreateAPIView):
    model = Passport
    serializer_class = PassportSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_profile = get_user_profile(request)
        request.data['creator'] = user_profile.id
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        user_profile = get_user_profile(self.request)
        return Passport.active.filter(creator=user_profile).order_by('-created_at')


class PassportDetail(generics.DestroyAPIView):
    model = Passport
    serializer_class = PassportSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_profile = get_user_profile(self.request)
        return Passport.active.filter(creator=user_profile)

    def destroy(self, request, *args, **kwargs):
        return mark_deleted(self)


class PassportBackdoor(generics.ListAPIView):
    """
    Returns passports for specified user

    Allow only for admin
    """

    model = Passport
    serializer_class = PassportSerializer
    permission_classes = (IsBackdoorAuthenticated,)
    queryset = Passport.active.all()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Passport.objects.filter(creator=user_id)
