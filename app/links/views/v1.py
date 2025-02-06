from django.contrib.postgres.aggregates import ArrayAgg
from django.shortcuts import redirect
from links import statistics
from links.models import ShortURL
from links.serializers.v1 import ShortURLSerializerV1, StatisticsSerializerV1
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class ShortURLViewSet(viewsets.GenericViewSet):
    serializer_class = ShortURLSerializerV1

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


@api_view(['GET'])
def redirect_to_original_link(request, token):
    short_link = get_object_or_404(ShortURL, token=token)
    statistics.log(request.META, short_link)
    return redirect(short_link.original, permanent=False)
