import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

import db_load
from ads.models import Category, Publication


def start_page(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class LoadDatabaseView(View):
    def post(self, request):
        request_data = json.loads(request.body)
        filename = request_data["filename"]
        json_list = json.loads(db_load.csv_to_json_from_me(filename))

        for item in json_list:
            if filename == "categories.csv":
                category = Category()
                category.name = item["name"]
                category.save()
            elif filename == "ads.csv":
                publication = Publication()
                publication.name = item["name"]
                publication.author = item["author"]
                publication.price = item["price"]
                publication.description = item["description"]
                publication.address = item["address"]
                publication.is_published = item["is_published"]
                publication.save()

        return HttpResponse(f"database {filename[:-4]} loaded")


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):

    def post(self, request):
        request_data = json.loads(request.body)
        new_category = Category()
        new_category.name = request_data["name"]
        new_category.save()

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
class PublicationView(View):

    def post(self, request):
        request_data = json.loads(request.body)
        new_publication = Publication()
        new_publication.author = request_data["author"]
        new_publication.price = int(request_data["price"])
        new_publication.description = request_data["description"]
        new_publication.address = request_data["address"]
        new_publication.is_published = request_data["is_published"]
        new_publication.save()

        return JsonResponse({
            "id": new_publication.id,
            "name": new_publication.name,
            "author": new_publication.author,
            "price": new_publication.price,
            "description": new_publication.description,
            "address": new_publication.address,
            "is_published": new_publication.is_published
        })

    def get(self, request):
        publications = Publication.objects.all()

        return JsonResponse([{
            "id": publication.id,
            "name": publication.name,
            "author": publication.author,
            "price": publication.price
        } for publication in publications], safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class PublicationDetailView(DetailView):
    model = Publication

    def get(self, request, *args, **kwargs):
        publication = self.get_object()

        return JsonResponse({
            "id": publication.id,
            "name": publication.name,
            "author": publication.author,
            "price": publication.price,
            "description": publication.description,
            "address": publication.address,
            "is_published": publication.is_published
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