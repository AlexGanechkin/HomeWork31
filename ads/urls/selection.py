from rest_framework import routers

from ads.views.selection import SelectionViewSet

# -------------------- берем из разбора --------------------------
router = routers.SimpleRouter()
router.register('', SelectionViewSet)

urlpatterns = router.urls
