from apps.youtube.models import YoutubeToken
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView


class YoutubeTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        token = YoutubeToken.active.first()
        if not token:
            return Response({'error': 'Token not found. Please, contact with task admin.'}, status=HTTP_404_NOT_FOUND)

        token.count += 1
        token.save()
        return Response({'token': token.token}, status=HTTP_200_OK)
