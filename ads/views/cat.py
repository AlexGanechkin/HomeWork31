import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Category

from rest_framework.viewsets import ModelViewSet

from ads.serializers.cat_serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#@method_decorator(csrf_exempt, name="dispatch")
#class CategoryListView(ListView):
#    model = Category
#
#    def get(self, request, *args, **kwargs):
#        super().get(request, *args, **kwargs)
#
#        self.object_list = self.object_list.order_by("name")
#
#        return JsonResponse([{
#            "id": category.id,
#            "name": category.name
#        } for category in self.object_list], safe=False, json_dumps_params={"ensure_ascii": False})
#
#
#@method_decorator(csrf_exempt, name="dispatch")
#class CategoryDetailView(DetailView):
#    model = Category
#
#    def get(self, request, *args, **kwargs):
#        super().get(request, *args, **kwargs)
#
#        return JsonResponse({
#            "id": self.object.id,
#            "name": self.object.name
#        }, safe=False, json_dumps_params={"ensure_ascii": False})
#
#
#@method_decorator(csrf_exempt, name="dispatch")
#class CategoryCreateView(CreateView):
#    model = Category
#    fields = ['name'] # можно указать что угодно, например, '__all__'
#
#    def post(self, request, *args, **kwargs):
#        request_data = json.loads(request.body)
#
#        new_category = Category.objects.create(name=request_data.get("name"))
#
#        return JsonResponse({
#            "id": new_category.id,
#            "name": new_category.name
#        })
#
#
#@method_decorator(csrf_exempt, name="dispatch")
#class CategoryUpdateView(UpdateView):
#    model = Category
#    fields = ['name', 'slug']
#
#    def patch(self, request, *args, **kwargs):
#        super().post(request, *args, **kwargs)
#
#        request_data = json.loads(request.body)
#        self.object.name = request_data.get('name')
#        self.object.slug = request_data.get('slug')
#        self.object.save()
#
#        return JsonResponse({
#            "id": self.object.id,
#            "name": self.object.name
#        }, safe=False, json_dumps_params={"ensure_ascii": False})
#
#
#@method_decorator(csrf_exempt, name="dispatch")
#class CategoryDeleteView(DeleteView):
#    model = Category
#    success_url = '/'
#
#    def delete(self, request, *args, **kwargs):
#        # cat = self.get_object()
#        super().delete(request, *args, **kwargs)
#
#        return JsonResponse({"status": "ok"}) # {"id": cat.id}
