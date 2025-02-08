from core.redis import redis_client as cache
from django.contrib.postgres.aggregates import ArrayAgg
from django.shortcuts import redirect
from links.models import ShortURL
from links.serializers.v1 import ShortenSerializerV1, StatisticsSerializerV1
from links.tasks import log_statistics
from rest_framework import status, views, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class ShortenViewSetV1(viewsets.GenericViewSet):
    serializer_class = ShortenSerializerV1

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        original_url = serializer.validated_data["original"]
        short_link, created = ShortURL.objects.get_or_create(original=original_url)

        return Response({"short_url": short_link.url}, status=status.HTTP_200_OK)


class StatisticsViewSetV1(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatisticsSerializerV1
    queryset = ShortURL.objects.annotate(
        ip_addresses=ArrayAgg("clicks__ip_address", distinct=True),
        user_agents=ArrayAgg("clicks__user_agent", distinct=True),
    )
    lookup_field = "token"


class RedirectViewV1(views.APIView):
    def get(self, request, token):
        short_link = get_object_or_404(ShortURL, token=token)

        log_statistics.delay(self._serializable_meta(), short_link.id)
        cache.incr(f"clicks:{short_link.token}")
        return redirect(short_link.original, permanent=False)

    def _serializable_meta(self):
        return {
            key: value
            for key, value in self.request.META.items()
            if isinstance(value, str)
        }
