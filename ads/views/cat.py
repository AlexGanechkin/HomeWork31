import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from ads.models import Category


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):

    def post(self, request):
        request_data = json.loads(request.body)
        new_category = Category()
        new_category.name = request_data["name"]
        new_category.save()
        # new_cat = Category.objects.create(name=data.get("name")) - вариант наставника

        return JsonResponse({
            "id": new_category.id,
            "name": new_category.name
        })

    def get(self, request):
        categories = Category.objects.all()

        return JsonResponse([{
            "id": category.id,
            "name": category.name
        } for category in categories], safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        }, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(ListView):
    model = Category
    """ Вьюху по выводу списка объектов оставил, но не подключил, т.к. на один рут нельзя подвесить разные generic view """
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        categories = self.object_list

        return JsonResponse([{
            "id": category.id,
            "name": category.name
        } for category in categories], safe=False, json_dumps_params={"ensure_ascii": False})