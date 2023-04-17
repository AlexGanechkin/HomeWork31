from rest_framework.viewsets import ModelViewSet

from ads.location_serializers import LocationSerializer
from ads.models import Location


class LocationView(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
