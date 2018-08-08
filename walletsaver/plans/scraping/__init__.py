"""
Scraping facilities.
This does not depend upon models, so the Manager should sync data.
It also was made to support any number of independent carriers.
"""
from typing import Generator

import requests

from plans.const import CARRIER_FASTWEB
from plans.scraping.domain import PlanData
from . import fastweb

SCRAPING_RULES = {
    CARRIER_FASTWEB: ('https://www.fastweb.it', fastweb),
}


def fetch_plans(carrier_id: int) -> Generator[PlanData, None, None]:
    """Scrapes a given carrier, extracting current site data.

    Args:
        carrier_id: the carrier constant.

    Returns:
        a generator with the fetched PlanDatas.

    Raises:
        KeyError: if the carrier is unknown.
    """

    # this could be a nice celery canvas chain, scheduled in `beat`,
    # running for all carriers in parallel:
    # workflow = group(
    #     chain(
    #         retrieve_page_content.s(carrier_id),
    #         parse_html.s(),
    #         store_model_plans.s(carrier_id),
    #     ) for url, find, extract in <RULES>
    # )
    # workflow()
    url, scraper = SCRAPING_RULES[carrier_id]
    data = retrieve_page_content(url)
    return scraper.parse_html(data)


def retrieve_page_content(url: str) -> str:
    """Fetches the content of a carrier url.

    Args:
        url: the carrier url.

    Returns:
        the result of a GET request in the url

    Raises:
        HTTPError: if the status is not 2xx or 3xx
    """
    r = requests.get(url)

    # this task would be scheduled for retrying later in case of error.
    r.raise_for_status()
    return r.text
