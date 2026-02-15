from __future__ import annotations

from dataclasses import dataclass

import httpx
import structlog

logger = structlog.get_logger()


@dataclass(frozen=True)
class InstanceHealth:
    reachable: bool
    response_time_seconds: float


@dataclass(frozen=True)
class PluginHealth:
    plugin_id: str
    healthy: bool
    response_time_seconds: float


class RHDHScraper:
    """
    async RHDH scraper handling all calls to get RHDH instance
    health metrics
    """

    def __init__(self, base_url: str, token: str = "") -> None:
        self._base_url = base_url.rstrip("/")
        headers: dict[str, str] = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=headers,
            timeout=10.0,
        )

    @property
    def name(self) -> str:
        return self._base_url

    async def check_instance_health(self) -> InstanceHealth:
        """
        check if the RHDH instance is reachable via its health endpoint
        """
        raise NotImplementedError("check_instance_health not implemented yet")

    async def check_plugins(self) -> list[PluginHealth]:
        """
        check health of each plugin by hitting its known endpoint.
        """
        raise NotImplementedError("check_plugins not implemented yet")

    async def close(self) -> None:
        await self._client.aclose()
