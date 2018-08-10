from rest_framework import generics

from plans.models import CarrierPlan
from plans.api.serializers import CarrierPlanSerializer
class CarrierPlanList(generics.ListAPIView):


class CarrierPlanDetail(generics.RetrieveAPIView):
    """Carrier plans detail mobile API."""
    queryset = CarrierPlan.objects.all()
    serializer_class = CarrierPlanSerializer
