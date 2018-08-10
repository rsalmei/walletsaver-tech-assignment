import operator
from decimal import Decimal

import pytest
from django.urls import reverse

from plans.models import CarrierPlan


@pytest.fixture
def data(db):
    CarrierPlan(
        id=1, carrier=1, title='internet', description='descr',
        current_price=Decimal('35.20'), old_price=Decimal()
    ).save()
    CarrierPlan(
        id=2, carrier=1, title='sky', description='descr',
        current_price=Decimal('48.99'), old_price=Decimal()
    ).save()
    CarrierPlan(
        id=3, carrier=1, title='mobile', description='descr',
        current_price=Decimal('12.50'), old_price=Decimal()
    ).save()


@pytest.fixture
def list_url(data):
    yield reverse('plans-list')


@pytest.fixture
def detail_url(data):
    yield reverse('plans-detail', args=(1,))


@pytest.mark.django_db
def test_api_list_exists(list_url, client):
    r = client.get(list_url)
    assert r.status_code == 200


@pytest.mark.django_db
def test_api_detail_exists(detail_url, client):
    r = client.get(detail_url)
    assert r.status_code == 200


@pytest.mark.parametrize('price_range, expected_ids', [
    ('', (1, 2, 3)),
    ('0', (1, 2, 3)),
    ('12.5', (1, 2, 3)),
    ('12.50', (1, 2, 3)),
    ('20', (1, 2)),
    ('20.', (1, 2)),
    ('20.0', (1, 2)),
    ('0,100', (1, 2, 3)),
    ('12,36', (1, 3)),
    ('10,40', (1, 3)),
    ('10.,40.', (1, 3)),
    ('10.0,40', (1, 3)),
    ('10,35.2', (1, 3)),
    ('10,35.20', (1, 3)),
    ('35,36', (1,)),
    ('48,49', (2,)),
    ('12,13', (3,)),
    ('12.5,12.5', (3,)),
    ('12.50,12.50', (3,)),
    ('1,2', ()),
    ('2,1', ()),
    ('100', ()),
])
@pytest.mark.django_db
def test_api_list_price_range(price_range, expected_ids, list_url, client):
    r = client.get(list_url, dict(price=price_range))
    op = operator.itemgetter('id')
    assert r.status_code == 200
    assert tuple(map(op, r.json())) == expected_ids


@pytest.mark.parametrize('price_range', [
    ',',
    '0,',
    '12.50,',
    '20.,',
    '20.0,',
    'rogerio',
    '0,rogerio',
    'rogerio,0',
    '!',
    'r,o',
    '!,!',
])
@pytest.mark.django_db
def test_api_list_price_range_invalid(price_range, list_url, client):
    r = client.get(list_url, dict(price=price_range))
    assert r.status_code == 400


@pytest.mark.parametrize('sort, expected_ids', [
    ('', (1, 2, 3)),
    ('1', (1, 2, 3)),
    ('rogerio', (1, 2, 3)),
    (':', (1, 2, 3)),
    ('name', (1, 3, 2)),
    ('name:', (1, 3, 2)),
    ('name:1', (1, 3, 2)),
    ('name:rogerio', (1, 3, 2)),
    ('name:asc', (1, 3, 2)),
    ('name:desc', (2, 3, 1)),
    ('price', (3, 1, 2)),
    ('price:', (3, 1, 2)),
    ('price:1', (3, 1, 2)),
    ('price:rogerio', (3, 1, 2)),
    ('price:asc', (3, 1, 2)),
    ('price:desc', (2, 1, 3)),
])
@pytest.mark.django_db
def test_api_list_sort(sort, expected_ids, list_url, client):
    r = client.get(list_url, dict(sort=sort))
    op = operator.itemgetter('id')
    assert r.status_code == 200
    assert tuple(map(op, r.json())) == expected_ids


@pytest.mark.parametrize('price_range, sort, expected_ids', [
    ('', 'name:asc', (1, 3, 2)),
    ('', 'name:desc', (2, 3, 1)),
    ('', 'price:asc', (3, 1, 2)),
    ('', 'price:desc', (2, 1, 3)),
    ('12.5', 'name:asc', (1, 3, 2)),
    ('12.5', 'name:desc', (2, 3, 1)),
    ('12.5', 'price:asc', (3, 1, 2)),
    ('12.5', 'price:desc', (2, 1, 3)),
    ('20', 'name:asc', (1, 2)),
    ('20', 'name:desc', (2, 1)),
    ('20', 'price:asc', (1, 2)),
    ('20', 'price:desc', (2, 1)),
    ('0,50', 'name:asc', (1, 3, 2)),
    ('0,50', 'name:desc', (2, 3, 1)),
    ('0,50', 'price:asc', (3, 1, 2)),
    ('0,50', 'price:desc', (2, 1, 3)),
    ('12,36', 'name:asc', (1, 3)),
    ('12,36', 'name:desc', (3, 1)),
    ('12,36', 'price:asc', (3, 1)),
    ('12,36', 'price:desc', (1, 3)),
    ('35,36', 'name:asc', (1,)),
    ('35,36', 'name:desc', (1,)),
    ('35,36', 'price:asc', (1,)),
    ('35,36', 'price:desc', (1,)),
    ('48,49', 'name:asc', (2,)),
    ('48,49', 'name:desc', (2,)),
    ('48,49', 'price:asc', (2,)),
    ('48,49', 'price:desc', (2,)),
    ('12,13', 'name:asc', (3,)),
    ('12,13', 'name:desc', (3,)),
    ('12,13', 'price:asc', (3,)),
    ('12,13', 'price:desc', (3,)),
    ('1,2', 'name:asc', ()),
    ('1,2', 'name:desc', ()),
    ('1,2', 'price:asc', ()),
    ('1,2', 'price:desc', ()),
    ('100', 'name:asc', ()),
    ('100', 'name:desc', ()),
    ('100', 'price:asc', ()),
    ('100', 'price:desc', ()),
])
@pytest.mark.django_db
def test_api_list_both_price_range_and_sort(price_range, sort, expected_ids, list_url, client):
    r = client.get(list_url, dict(price=price_range, sort=sort))
    op = operator.itemgetter('id')
    assert r.status_code == 200
    assert tuple(map(op, r.json())) == expected_ids

