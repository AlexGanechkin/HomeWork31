from django.urls import path

from ads.views.cat import *

urlpatterns = [
    path('', CategoryView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
]
