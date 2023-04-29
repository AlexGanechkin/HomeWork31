from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Selection
from ads.serializers.ad_serializers import AdListSerializer
from ads.serializers.permissions import IsOwner
from ads.serializers.sel_serializers import SelectionListSerializer, SelectionSerializer, SelectionCreateSerializer, \
    SelectionDetailSerializer


# -------------------------- берем с разбора ----------------------------------------

class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.order_by('name')
    default_serializer_class = SelectionSerializer

    default_permission = [AllowAny]
    permissions = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner],
        "partial_update": [IsAuthenticated, IsOwner],
        "destroy": [IsAuthenticated, IsOwner],
    }

    serializers = {
        'list': SelectionListSerializer,
        'create': SelectionCreateSerializer,
        'retrieve': SelectionDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]


# ------------------------- это я пытаюсь писать сам ---------------------------------
class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer

    # def get(self, request, *args, **kwargs):
    #     vacancy_text = request.GET.get('text', None)
    #     if vacancy_text:
    #         self.queryset = self.queryset.filter(
    #             text__icontains=vacancy_text
    #         )


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    #permission_classes = [IsAuthenticated]


"""
class VacancyCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
"""
