from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from links.views import RedirectLinkAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'
         ),
    path('auth/', include('authentication.urls')),
    path('links/', include('links.urls')),
    path('users/', include('users.urls')),
    path('<str:domain>/', RedirectLinkAPIView.as_view(), name='redirect-link'),
]

urlpatterns += [
    path("", RedirectView.as_view(url="/api/docs/", permanent=True)),
]
