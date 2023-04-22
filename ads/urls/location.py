from rest_framework import routers

from ads.views.location import LocationView

router = routers.SimpleRouter()
router.register('location', LocationView)

urlpatterns = router.urls

