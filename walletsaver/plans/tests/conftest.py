import pytest

from plans.const import CARRIER_FASTWEB
from plans.tests.modelfactory import CarrierPlanFactory


@pytest.fixture(params=(CARRIER_FASTWEB,))
def carrier_id(request):
    return request.param


@pytest.fixture(params=(-1, 42, 1e10))
def invalid_carrier_id(request):
    return request.param


@pytest.fixture(scope='session')
def plan_factory():
    def _factory(**kwargs):
        return CarrierPlanFactory.build(**kwargs)

    return _factory


@pytest.fixture(scope='session')
def plan_factory_db():
    def _factory(**kwargs):
        return CarrierPlanFactory.create(**kwargs)

    return _factory
