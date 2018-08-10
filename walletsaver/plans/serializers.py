from rest_framework import serializers

from plans.models import CarrierPlan


class CarrierPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierPlan
        fields = ('id', 'carrier', 'title', 'description', 'current_price', 'old_price')
