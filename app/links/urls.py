from django.urls import path
from .views import LinkCreateAPIView

urlpatterns = [
    path('', LinkCreateAPIView.as_view(), name='create_link'),
]
