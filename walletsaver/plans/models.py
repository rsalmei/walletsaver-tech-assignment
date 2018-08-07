from django.db import models

from plans.const import CARRIER_FASTWEB


class CarrierPlanQuerySet(models.QuerySet):
    def from_carrier(self, carrier_id):
        return self.filter(carrier=carrier_id)


class CarrierPlanManager(models.Manager):
    pass

class CarrierPlan(models.Model):
    PROVIDERS = (
        (CARRIER_FASTWEB, 'fastweb'),
    )

    carrier = models.IntegerField(choices=PROVIDERS)
    title = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=60)
    current_price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2)

    objects = CarrierPlanManager.from_queryset(CarrierPlanQuerySet)()

    def __str__(self):
        return '#{} {}:{}'.format(self.id, self.get_carrier_display(), self.title)
