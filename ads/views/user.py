import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView

from Application import settings
from ads.models import User, Location
from ads.serializers import UserCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_list = paginator.get_page(page_number)

        users = []
        for user in page_list:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.location_id.all()))
            })

        response = {
            "items": users,
            "total": paginator.num_pages,
            "num_pages": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "location": list(map(str, self.object.location_id.all()))
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailListView(View):
    def get(self, request):
        counted_users = User.objects.annotate(publications=Count('publication', filter=Q(publication__is_published=True)))

        counted_users = counted_users.prefetch_related('location_id').order_by("username")

        paginator = Paginator(counted_users, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.location_id.all())),
                "total_ads": user.publications
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'location_id']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        request_data = json.loads(request.body)
        # добавляем if'ы
        if "username" in request_data:
            self.object.username = request_data.get('username')
        self.object.password = request_data['password']
        self.object.first_name = request_data['first_name']
        self.object.last_name = request_data['last_name']
        self.object.age = int(request_data['age'])

        # self.object.location_id.clear() # чистим локации перед добавлением новых
        for location in request_data['locations']:
            location_obj, created = Location.objects.get_or_create(name=location)
            self.object.location_id.add(location_obj)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "age": self.object.age,
            "locations": list(map(str, self.object.location_id.all()))
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})
