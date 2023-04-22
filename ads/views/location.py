from rest_framework.viewsets import ModelViewSet

from ads.serializers.location_serializers import LocationSerializer
from ads.models import Location


class LocationView(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    # Вариант наставника, он делал на публикациях, я для примера переписал код сюда
    def list(self, request, *args, **kwargs):
        locations = request.GET.getlist('id', [])
        if locations:
            self.queryset = self.queryset.filter(id__in=locations)

        return super().list(request, *args, **kwargs)
