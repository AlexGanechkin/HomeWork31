import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Publication


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
        # new_cat = Publication.objects.create(**data) - вариант наставника

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
