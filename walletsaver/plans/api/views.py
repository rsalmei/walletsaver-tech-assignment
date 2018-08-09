from rest_framework import viewsets

from plans.models import CarrierPlan
from plans.api.serializers import CarrierPlanSerializer


class CarrierPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Carrier plans mobile API, readonly list and detail actions only."""
    queryset = CarrierPlan.objects.all()
    serializer_class = CarrierPlanSerializer
