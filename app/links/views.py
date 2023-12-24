from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Link
from .serializers import LinkSerializer


class LinkCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LinkSerializer(data=request.data)

        if serializer.is_valid():
            link = Link.objects.create(id=serializer.validated_data['id'],
                                       user=request.user, url=request.url)
            return Response({'id': link.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
