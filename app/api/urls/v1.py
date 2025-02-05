from django.urls import include, path
from links.views.v1 import ShortURLViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("shorten", ShortURLViewSet, basename="short-url")

urlpatterns = [
    path("", include(router.urls)),
]
