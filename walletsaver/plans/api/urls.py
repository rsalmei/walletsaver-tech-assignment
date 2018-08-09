from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# in a real project, there would be a `carriers` also.
router.register(r'plans', views.CarrierPlanViewSet, base_name='carrierplans')

urlpatterns = router.urls
