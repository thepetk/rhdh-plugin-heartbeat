import pytest

from rhdh_plugin_heartbeat.scraper import RHDHScraper


@pytest.fixture
def base_url() -> "str":
    return "https://rhdh.example.com"


@pytest.fixture
def scraper(base_url: str) -> "RHDHScraper":
    return RHDHScraper(base_url=base_url, token="test-token")
