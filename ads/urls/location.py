from django.urls import path, include
from rest_framework import routers

from ads.views.location import LocationView

router = routers.SimpleRouter()
router.register('location', LocationView)

urlpatterns = [
    path('', include(router.urls)),
]
