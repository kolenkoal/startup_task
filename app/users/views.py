from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import SerializerMethodField

from links.models import Link
from links.serializers import LinkDetailSerializer


class UserLinksAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LinkDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Link.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
