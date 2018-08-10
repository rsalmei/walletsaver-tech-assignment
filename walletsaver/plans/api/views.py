from decimal import Decimal, InvalidOperation

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.exceptions import ParseError

from plans.api.serializers import CarrierPlanSerializer
from plans.models import CarrierPlan


class CarrierPlanList(generics.ListAPIView):
    """Carrier plans list mobile API, with filtering and ordering."""
    serializer_class = CarrierPlanSerializer

    def get_queryset(self):
        qs = CarrierPlan.objects.all()

        price_range = self.request.query_params.get('price')
        if price_range:
            qs = self.set_price_range(price_range, qs)

        sort_by = self.request.query_params.get('sort', '')
        qs = self.set_order_by(sort_by, qs)

        return qs

    def set_price_range(self, value: str, qs: QuerySet):
        try:
            value = tuple(map(Decimal, value.split(',')))
            if len(value) > 2:
                raise ValueError()
        except InvalidOperation:
            raise ParseError('price should be [int[,int]]')
        else:
            if len(value) == 2:
                return qs.filter(current_price__range=value)
            return qs.filter(current_price__gte=value[0])

    def set_order_by(self, value: str, qs: QuerySet):
        field, _, direction = value.partition(':')
        fields = dict(price='current_price', name='title')
        directions = dict(desc='-')
        return qs.order_by(directions.get(direction, '') + fields.get(field, 'id'))


class CarrierPlanDetail(generics.RetrieveAPIView):
    """Carrier plans detail mobile API."""
    queryset = CarrierPlan.objects.all()
    serializer_class = CarrierPlanSerializer
