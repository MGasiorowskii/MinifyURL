from django.urls import include, path
from links.views.v1 import ShortURLViewSet, redirect_to_original_link
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("shorten", ShortURLViewSet, basename="short-url")

urlpatterns = [
    path("", include(router.urls)),
    path(
        'redirect/<str:token>/',
        redirect_to_original_link,
        name='redirect-to-original-link',
    ),
]
