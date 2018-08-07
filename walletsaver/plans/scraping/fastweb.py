from itertools import repeat
from typing import Generator, Optional

from bs4 import BeautifulSoup, Tag

from plans.scraping.domain import PlanData

HTML_CLASSES = ('product', 'description', 'hilite', 'small')


def parse_html(page: str) -> Generator[PlanData, None, None]:
    """Extracts data from this carrier."""
    soup = BeautifulSoup(page, 'html.parser')
    data = soup.find_all('a', class_='menulink')
    yield from filter(None, map(extract_plan, data))


def extract_plan(tag: Tag) -> Optional[PlanData]:
    """Extracts a plan data from a tag."""
    extracted = map(extract_field, repeat(tag), HTML_CLASSES)
    try:
        return PlanData._make(extracted)
    except AttributeError:
        pass


def extract_field(tag: Tag, html_class: str) -> str:
    """Extracts a particular field from a tag."""
    return ''.join(tag.find('span', class_=html_class).strings)
