"""Pluggable search providers for company intel.

Every result carries source URLs. Providers:
- FixtureProvider: offline canned results (tests, CI, demos without network)
- DuckDuckGoProvider: live HTML search (no login, no scraping of walled sites)
"""
from dataclasses import dataclass, field


@dataclass
class IntelItem:
    title: str
    url: str
    snippet: str
    kind: str  # "interview-experience" | "oa-question" | "news" | "glassdoor-like"
    source: str  # provider name
    model_written: bool = False


class SearchProvider:
    name = "base"

    def search(self, query: str, limit: int = 10) -> list[IntelItem]:
        raise NotImplementedError


def get_provider(name: str | None = None) -> SearchProvider:
    import os
    name = name or os.environ.get("MOCKMATE_SEARCH", "fixture")
    if name == "duckduckgo":
        from .duckduckgo import DuckDuckGoProvider
        return DuckDuckGoProvider()
    from .fixture import FixtureProvider
    return FixtureProvider()
