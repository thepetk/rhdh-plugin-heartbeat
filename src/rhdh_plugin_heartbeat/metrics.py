from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

from rhdh_plugin_heartbeat.scraper import InstanceHealth, PluginHealth

instance_up = Gauge(
    "rhdh_heartbeat_instance_up",
    "Whether the RHDH instance is reachable (1=up, 0=down)",
    ["instance"],
)

instance_response_time = Histogram(
    "rhdh_heartbeat_instance_response_time_seconds",
    "Response time of the RHDH instance health check",
    ["instance"],
)

plugin_up = Gauge(
    "rhdh_heartbeat_plugin_up",
    "Whether a plugin is healthy (1=up, 0=down)",
    ["instance", "plugin"],
)

plugin_response_time = Histogram(
    "rhdh_heartbeat_plugin_response_time_seconds",
    "Response time of a plugin health check",
    ["instance", "plugin"],
)

scrape_duration = Histogram(
    "rhdh_heartbeat_scrape_duration_seconds",
    "Total duration of a scrape cycle",
)

scrape_errors_total = Counter(
    "rhdh_heartbeat_scrape_errors_total",
    "Total number of scrape errors",
    ["stage"],
)


def update_instance_metrics(instance: str, health: InstanceHealth) -> None:
    instance_up.labels(instance=instance).set(1 if health.reachable else 0)
    instance_response_time.labels(instance=instance).observe(
        health.response_time_seconds
    )


def update_plugin_metrics(instance: str, results: list[PluginHealth]) -> None:
    for plugin in results:
        plugin_up.labels(instance=instance, plugin=plugin.plugin_id).set(
            1 if plugin.healthy else 0
        )
        plugin_response_time.labels(instance=instance, plugin=plugin.plugin_id).observe(
            plugin.response_time_seconds
        )
