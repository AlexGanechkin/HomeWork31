from django.http import JsonResponse
from django.shortcuts import render


def start_page(request):
    return JsonResponse({"status": "ok"})
