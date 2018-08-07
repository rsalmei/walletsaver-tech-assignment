from unittest import mock

import pytest
import os
from plans.scraping import PlanData
from plans.scraping.fastweb import parse_html, extract_plan, extract_field


@pytest.fixture(scope='session')
def page():
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'fixture_fastweb.html')) as f:
        yield f.read()


def test_fastweb_total(page):
    gen = parse_html(page)
    result = next(gen)
    with pytest.raises(StopIteration):
        next(gen)

    assert result == PlanData(product='INTERNET',
                              description='Internet illimitato fino ad 1 Gbit/s senza Telefono, profilo Gaming',
                              current_price='24,95€/mese',
                              old_price='anziché 29,95€')

def test_fastweb_parse_html():
    pass
