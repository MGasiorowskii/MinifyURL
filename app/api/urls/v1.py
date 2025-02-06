from django.urls import include, path
from links.views.v1 import (
    ShortenViewSetV1,
    StatisticsViewSetV1,
    redirect_to_original_link,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("shorten", ShortenViewSetV1, basename="short-url")
router.register("statistics", StatisticsViewSetV1, basename="statistics")

urlpatterns = [
    path("", include(router.urls)),
    path(
        'redirect/<str:token>/',
        redirect_to_original_link,
        name='redirect-to-original-link',
    ),
]
