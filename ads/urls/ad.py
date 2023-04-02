from django.urls import path

from ads.views.ad import *

urlpatterns = [
    path('', PublicationView.as_view()),
    path('<int:pk>/', PublicationDetailView.as_view()),
]
