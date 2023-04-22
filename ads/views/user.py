

from django.db.models import Count, Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from ads.models import User
from ads.serializers.serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer, UserListSerializer


class UserListView(ListAPIView):
    queryset = User.objects.annotate(total_ads=Count('publication', filter=Q(publication__is_published=True))).order_by("username")
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
