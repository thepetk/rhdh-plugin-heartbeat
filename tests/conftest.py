import pytest

from rhdh_plugin_heartbeat.config import Config


@pytest.fixture
def default_config() -> "Config":
    return Config(
        listen_address=":9185",
        scrape_interval=5,
        log_level="debug",
        rhdh_base_url="https://rhdh.example.com",
        rhdh_token="test-token",
    )
