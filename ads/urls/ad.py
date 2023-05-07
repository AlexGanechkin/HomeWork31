
from django.urls import path
from rest_framework import routers

from ads.views.ad import *

router = routers.SimpleRouter()
router.register('', AdviewSet)
urlpatterns = router.urls

#urlpatterns = [
#    path('', PublicationListView.as_view()),
#    path('<int:pk>/', PublicationDetailView.as_view()),
#    path('create/', PublicationCreateView.as_view()),
#    path('<int:pk>/update/', PublicationUpdateView.as_view()),
#    path('<int:pk>/delete/', PublicationDeleteView.as_view()),
#    path('<int:pk>/image/', PublicationUpdateImageView.as_view()),
#]
#
#urlpatterns += router.urls
