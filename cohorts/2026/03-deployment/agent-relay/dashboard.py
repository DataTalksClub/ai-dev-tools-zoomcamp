"""Dashboard asset loading.

Keeping the HTML as an asset makes it straightforward to replace the starter
dashboard without mixing presentation code into the API routes.
"""

from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=1)
def dashboard_html() -> str:
    return Path(__file__).with_name("dashboard.html").read_text(encoding="utf-8")


__all__ = ["dashboard_html"]
