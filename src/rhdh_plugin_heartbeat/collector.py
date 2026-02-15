from __future__ import annotations

import asyncio
import time

import structlog

from rhdh_plugin_heartbeat.config import Config
from rhdh_plugin_heartbeat.metrics import (
    scrape_duration,
    scrape_errors_total,
    update_instance_metrics,
    update_plugin_metrics,
)
from rhdh_plugin_heartbeat.scraper import RHDHScraper

logger = structlog.get_logger()


async def run_collector(
    config: Config,
    scraper: RHDHScraper,
    stop_event: asyncio.Event,
) -> None:
    """
    handles the collection loop until stop_event is set.
    """
    logger.info(
        "collector_started",
        interval=config.scrape_interval,
    )

    while not stop_event.is_set():
        # monotonic is used to measure elapsed time without being affected
        # by system clock changes
        # https://docs.python.org/3/library/time.html#time.monotonic
        start = time.monotonic()
        try:
            # important to use await here so we can yield
            # control to check if stop_event is set
            health = await scraper.check_instance_health()
            update_instance_metrics(scraper.name, health)

            plugin_results = await scraper.check_plugins()
            update_plugin_metrics(scraper.name, plugin_results)

        except Exception:
            logger.exception("scrape_failed")
            scrape_errors_total.labels(stage="collect").inc()
        finally:
            elapsed = time.monotonic() - start
            scrape_duration.observe(elapsed)
            logger.debug("scrape_complete", duration=elapsed)

        try:
            # wait until scrape interval or stop_event is set,
            # whichever comes first
            await asyncio.wait_for(stop_event.wait(), timeout=config.scrape_interval)
        except TimeoutError:
            pass
