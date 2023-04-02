import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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
