from django.urls import path
from .views import UserLinksAPIView

urlpatterns = [
    path('me/', UserLinksAPIView.as_view(), name='user-links'),
]
