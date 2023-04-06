import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Application import settings
from ads.models import User, Location


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.prefetch_related('location_id').order_by("id")

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
                "locations": list(map(str, user.location_id.all()))
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
            "locations": list(map(str, self.object.location_id.all()))
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)

        new_user = User()
        new_user.username = request_data['username']
        new_user.password = request_data['password']
        new_user.first_name = request_data['first_name']
        new_user.last_name = request_data['last_name']
        new_user.role = request_data['role']
        new_user.age = int(request_data['age'])
        new_user.save()

        for location in request_data['locations']:
            location_obj, created = Location.objects.get_or_create(name=location)
            new_user.location_id.add(location_obj)

        new_user.save()

        return JsonResponse({
            "id": new_user.id,
            "username": new_user.username,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "role": new_user.role,
            "age": new_user.age,
            "locations": list(map(str, new_user.location_id.all()))
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        request_data = json.loads(request.body)
        self.object.username = request_data['username']
        self.object.password = request_data['password']
        self.object.first_name = request_data['first_name']
        self.object.last_name = request_data['last_name']
        self.object.age = int(request_data['age'])

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
