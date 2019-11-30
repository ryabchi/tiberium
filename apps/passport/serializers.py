from apps.passport.models import Passport
from rest_framework import serializers


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ('id', 'name', 'secret', 'creator', 'created_at')
        read_only_fields = ('id', 'created_at')
