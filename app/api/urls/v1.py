from django.urls import include, path
from links.views.v1 import RedirectViewV1, ShortenViewSetV1, StatisticsViewSetV1
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("shorten", ShortenViewSetV1, basename="short-url")
router.register("statistics", StatisticsViewSetV1, basename="statistics")

urlpatterns = [
    path("", include(router.urls)),
    path(
        'redirect/<str:token>/',
        RedirectViewV1.as_view(),
        name='redirect-url',
    ),
]
