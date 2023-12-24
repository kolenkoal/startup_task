from string import ascii_letters
from random import choice
from django.utils import timezone

from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Link
from .serializers import LinkSerializer


def generate_unique_id(length=8):
    characters = ascii_letters
    while True:
        unique_id = ''.join(choice(characters) for _ in range(length))
        if not Link.objects.filter(id=unique_id).exists():
            return unique_id


class LinkCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LinkSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            unique_id = generate_unique_id()
            link = Link.objects.create(id=unique_id,
                                       user=request.user,
                                       url=request.data["url"])
            return Response({'id': link.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectLinkAPIView(APIView):
    def get(self, request, domain):
        try:
            link = Link.objects.get(id=domain)
            link.last_accessed = timezone.now()
            link.save(update_fields=['last_accessed'])
            return redirect(link.url)
        except Link.DoesNotExist:
            return Response({'detail': 'Link not found'},
                            status=status.HTTP_404_NOT_FOUND)
