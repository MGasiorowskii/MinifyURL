from links.models import ShortURL
from links.serializers import ShortURLSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response


class ShortURLViewSet(viewsets.GenericViewSet):
    serializer_class = ShortURLSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        original_url = serializer.validated_data["original"]
        short_link, created = ShortURL.objects.get_or_create(original=original_url)

        return Response({"short_url": short_link.url}, status=status.HTTP_200_OK)
