from django.urls import path

from links.views import RedirectLinkAPIView
from . import views

urlpatterns = [
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
]
