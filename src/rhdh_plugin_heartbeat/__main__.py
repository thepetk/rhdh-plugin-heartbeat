from __future__ import annotations

import asyncio
import signal

import structlog
from prometheus_client import start_http_server

from rhdh_plugin_heartbeat.cli import parse_args
from rhdh_plugin_heartbeat.collector import run_collector
from rhdh_plugin_heartbeat.config import Config
from rhdh_plugin_heartbeat.logging import setup_logging
from rhdh_plugin_heartbeat.scraper import RHDHScraper


def main() -> None:
    args = parse_args()
    config = Config.from_args(args)

    setup_logging(config.log_level)
    logger = structlog.get_logger()

    if not config.rhdh_base_url:
        logger.error("rhdh_base_url is required (--rhdh.base-url or RHDH_BASE_URL)")
        raise SystemExit(1)

    port = config.listen_port
    # starting a prometheus client based on docs:
    # https://prometheus.github.io/client_python/exporting/http/
    start_http_server(port)
    logger.info("metrics_server_started", port=port)

    scraper = RHDHScraper(base_url=config.rhdh_base_url, token=config.rhdh_token)
    # creating an event so we can handle graceful shutdown on SIGINT/SIGTERM
    stop_event = asyncio.Event()

    async def _run() -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            # setting the event will release the event
            # loop currently running
            loop.add_signal_handler(sig, stop_event.set)

        try:
            await run_collector(config, scraper, stop_event)
        finally:
            await scraper.close()
            logger.info("shutdown_complete")

    asyncio.run(_run())


if __name__ == "__main__":
    main()
