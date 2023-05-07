
from django.urls import path
from rest_framework import routers
from ads.views.cat import *

#urlpatterns = [
#    path('', CategoryListView.as_view(), name="all_category"),
#    path('<int:pk>/', CategoryDetailView.as_view(), name="detail_category"),
#    path('create/', CategoryCreateView.as_view()),
#    path('<int:pk>/update/', CategoryUpdateView.as_view()),
#    path('<int:pk>/delete/', CategoryDeleteView.as_view()),
#]

router = routers.SimpleRouter()
router.register('', CategoryViewSet)
urlpatterns = router.urls
