import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    listen_address: "str" = ":9185"
    scrape_interval: "int" = 30
    log_level: "str" = "info"
    rhdh_base_url: "str" = ""
    rhdh_token: "str" = ""

    @property
    def listen_port(self) -> "int":
        """
        extracts port number from listen_address (e.g. ':9185' -> 9185).
        """
        return int(self.listen_address.rsplit(":", 1)[-1])

    @staticmethod
    def from_args(args: "object") -> "Config":
        """
        builds Config from parsed argparse namespace, with env var fallbacks.
        """
        return Config(
            listen_address=getattr(args, "listen_address"),
            scrape_interval=getattr(args, "scrape_interval"),
            log_level=getattr(args, "log_level"),
            rhdh_base_url=getattr(args, "rhdh_base_url")
            or os.environ.get("RHDH_BASE_URL", ""),
            rhdh_token=os.environ.get("RHDH_TOKEN", ""),
        )
