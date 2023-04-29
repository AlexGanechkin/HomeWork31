import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from Application import settings
from ads.models import Publication, User, Category
from ads.serializers.ad_serializers import AdSerializer, AdListSerializer, AdDetailSerializer
from ads.serializers.permissions import IsOwner, IsStaff


# Вариант наставника
class AdviewSet(ModelViewSet):
    queryset = Publication.objects.order_by('-price')
    default_serializer_class = AdSerializer

    default_permission = [AllowAny]
    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsStaff],
        "partial_update": [IsAuthenticated, IsOwner | IsStaff],
        "destroy": [IsAuthenticated, IsOwner | IsStaff],
    }

    serializers = {
        'list': AdListSerializer,
        'create': AdListSerializer,
        'retrieve': AdDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def list(self, request, *args, **kwargs):
        ads = request.GET.getlist('id', [])
        if ads:
            self.queryset = self.queryset.filter(id__in=ads)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class PublicationListView(ListView):
    model = Publication

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('author_id').order_by("-price")

        # ищем объявления, содержащие искомый текст в наименовании объявления: ?text=text
        text_request = request.GET.get('text')

        if text_request:
            self.object_list = self.object_list.filter(name__icontains=text_request)

        # ищем объявления, соответствующие id определенной категории: ?cat=1
        category_request = request.GET.get('cat')
        if category_request and category_request.isdigit():
            self.object_list = self.object_list.filter(category_id__id__exact=int(category_request))

        # ищем объявления с пользователями из определенной локации: ?location=location
        location_request = request.GET.get('location')
        if location_request:
            self.object_list = self.object_list.filter(author_id__location_id__name__icontains=location_request)

        # ищем объявления по диапазону цен: ?price_from=100&price_to=1000
        price_from_request = request.GET.get('price_from')
        if price_from_request:
            self.object_list = self.object_list.filter(price__gte=price_from_request)

        price_to_request = request.GET.get('price_to')
        if price_to_request:
            self.object_list = self.object_list.filter(price__lte=price_to_request)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_list = paginator.get_page(page_number)

        publications = []
        for publication in page_list:
            publications.append({
                    "id": publication.id,
                    "name": publication.name,
                    "author": publication.author_id.username,
                    "price": publication.price
                })

        response = {
            "items": publications,
            "total": paginator.num_pages,
            "num_pages": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class PublicationDetailView(RetrieveAPIView):
    queryset = Publication.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]
"""
@method_decorator(csrf_exempt, name="dispatch")
class PublicationDetailView(DetailView):
    model = Publication

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id.id,
            "author": self.object.author_id.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id.id,
            # "address": [loc.name for loc in self.object.author_id.location_id.all()],
            "image": self.object.image.url if self.object.image else None
        }, safe=False, json_dumps_params={"ensure_ascii": False})
"""


@method_decorator(csrf_exempt, name="dispatch")
class PublicationCreateView(CreateView):
    model = Publication
    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'category_id']

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)

        # вариант наставника
        # author = get_object_or_404(User, pk=request_data.pop('author_id'))
        # category = get_object_or_404(Category, pk=request_data.pop('category_id'))
        # new_publication = Publication.objects.create(author_id=author, category_id=category, **request_data)

        new_publication = Publication.objects.create(
            name=request_data["name"],
            author_id=get_object_or_404(User, pk=request_data['author_id']),
            price=int(request_data["price"]),
            description=request_data["description"],
            is_published=request_data["is_published"],
            category_id=get_object_or_404(Category, pk=request_data['category_id'])
        )

        return JsonResponse({
            "id": new_publication.id,
            "name": new_publication.name,
            "author": new_publication.author_id.username,
            "price": new_publication.price,
            "description": new_publication.description,
            "is_published": new_publication.is_published
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class PublicationUpdateImageView(UpdateView):
    model = Publication
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id.id,
            "author": self.object.author_id.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id.id,
            "image": self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class PublicationUpdateView(UpdateView):
    model = Publication
    fields = ['name', 'author_id', 'price', 'description', 'category_id']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        request_data = json.loads(request.body)

        if "name" in request_data:
            self.object.name = request_data.get('name')
        if "author_id" in request_data:
            self.object.author_id = get_object_or_404(User, pk=request_data.get('author_id'))
        # дальше if'ы вставлять не стал
        self.object.price = int(request_data['price'])
        self.object.description = request_data['description']
        self.object.category_id = get_object_or_404(Category, pk=request_data['category_id'])
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id.id,
            "author": self.object.author_id.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id.id,
            "image": self.object.image.url if self.object.image else None
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class PublicationDeleteView(DeleteView):
    model = Publication
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})
