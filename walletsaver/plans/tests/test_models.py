from unittest import mock

import pytest

from plans.models import CarrierPlan
from plans.scraping import PlanData


@pytest.fixture(scope='session')
def plan_qs():
    yield CarrierPlan.objects.none()


def test_plans_carrierplanqueryset_from_carrier(plan_qs):
    with mock.patch.object(plan_qs, 'filter') as mqsf:
        plan_qs.from_carrier(32)

    mqsf.assert_called_once_with(carrier=32)


@pytest.mark.django_db
def test_plans_carrierplanmanager_resync_plans(plan_factory_db):
    plan_factory_db(carrier=5)
    num = CarrierPlan.objects.from_carrier(5).count()
    plan_factory_db(carrier=12, title='nope')
    plan_factory_db(carrier=12, title='never')

    with mock.patch('plans.models.fetch_plans') as mfp:
        mfp.return_value = (PlanData('yes', 'descr', 1, 2),)
        CarrierPlan.objects.resync_plans(12)

    assert CarrierPlan.objects.from_carrier(12).count() == 1
    assert CarrierPlan.objects.from_carrier(5).count() == num


@pytest.mark.django_db
def test_plans_carrierplanmanager_resync_plans_error(invalid_carrier_id, plan_factory_db):
    plan_factory_db()
    num = CarrierPlan.objects.count()
    with pytest.raises(KeyError):
        CarrierPlan.objects.resync_plans(invalid_carrier_id)

    # guarantees no object was deleted.
    assert num == CarrierPlan.objects.count()
