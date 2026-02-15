import argparse


def parse_args(argv: "list[str] | None" = None) -> "argparse.Namespace":
    parser = argparse.ArgumentParser(
        prog="rhdh-plugin-heartbeat",
        description=(
            "Prometheus exporter for Red Hat Developer Hub instance and plugin health"
        ),
    )
    parser.add_argument(
        "--web.listen-address",
        dest="listen_address",
        default=":9185",
        help="Address to listen on for metrics (default: :9185)",
    )
    parser.add_argument(
        "--scrape.interval",
        dest="scrape_interval",
        type=int,
        default=30,
        help="Scrape interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--log.level",
        dest="log_level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Log level (default: info)",
    )
    parser.add_argument(
        "--rhdh.base-url",
        dest="rhdh_base_url",
        default="",
        help="Base URL of the RHDH instance (or set RHDH_BASE_URL)",
    )

    return parser.parse_args(argv)
