from unittest import mock

import pytest
from requests import HTTPError

from plans import scraping
from plans.const import CARRIER_FASTWEB


@pytest.fixture(params=(CARRIER_FASTWEB,))
def carrier_id(request):
    return request.param


@pytest.fixture(params=(-1, 42, 1e10))
def invalid_carrier_id(request):
    return request.param


@mock.patch('plans.scraping.retrieve_page_content')
def test_scraping_fetch_plans(mretrieve: mock.Mock, carrier_id: int):
    with mock.patch.dict('plans.scraping.SCRAPING_RULES',
                         values={carrier_id: ('url', mock.Mock())}):
        scraping.fetch_plans(carrier_id)
        url, scraper = scraping.SCRAPING_RULES[carrier_id]

    mretrieve.assert_called_once_with('url')
    scraper.parse_html.assert_called_once_with(mretrieve())


def test_scraping_fetch_plans_invalid(invalid_carrier_id: int):
    with pytest.raises(KeyError):
        scraping.fetch_plans(invalid_carrier_id)


@mock.patch('plans.scraping.requests')
def test_scraping_retrieve_page_content(mreqs: mock.Mock):
    r = mreqs.get.return_value = mock.Mock()
    result = scraping.retrieve_page_content('url')
    mreqs.get.assert_called_once_with('url')
    assert result == r.text


@mock.patch('plans.scraping.requests')
def test_scraping_retrieve_page_content_error(mreqs: mock.Mock):
    r = mreqs.get.return_value = mock.Mock()
    r.raise_for_status.side_effect = HTTPError
    with pytest.raises(HTTPError):
        scraping.retrieve_page_content('url')
    mreqs.get.assert_called_once_with('url')
    r.text.assert_not_called()
