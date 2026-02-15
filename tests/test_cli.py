from rhdh_plugin_heartbeat.cli import parse_args
from rhdh_plugin_heartbeat.config import Config


def test_parse_defaults():
    args = parse_args([])
    assert args.listen_address == ":9185"
    assert args.scrape_interval == 30
    assert args.log_level == "info"


def test_parse_custom_args():
    args = parse_args(
        [
            "--web.listen-address",
            ":8080",
            "--scrape.interval",
            "10",
            "--log.level",
            "debug",
            "--rhdh.base-url",
            "https://rhdh.example.com",
        ]
    )
    assert args.listen_address == ":8080"
    assert args.scrape_interval == 10
    assert args.log_level == "debug"
    assert args.rhdh_base_url == "https://rhdh.example.com"


def test_config_from_args():
    args = parse_args(
        [
            "--rhdh.base-url",
            "https://rhdh.example.com",
        ]
    )
    config = Config.from_args(args)
    assert config.rhdh_base_url == "https://rhdh.example.com"
    assert config.listen_port == 9185
