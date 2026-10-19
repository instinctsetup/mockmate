"""Offline fixture provider: canned, clearly-sourced intel for tests/CI."""
from .base import IntelItem, SearchProvider


class FixtureProvider(SearchProvider):
    name = "fixture"

    def search(self, query: str, limit: int = 10) -> list[IntelItem]:
        q = query.lower()
        items = []
        if "razorpay" in q:
            items = [
                IntelItem("Razorpay SDE interview experience (GeeksforGeeks)",
                          "https://www.geeksforgeeks.org/razorpay-interview-experience/",
                          "DSA rounds with graph and DP focus; one system-design round for experienced hires.",
                          "interview-experience", "fixture"),
                IntelItem("Razorpay engineering blog",
                          "https://engineering.razorpay.com/",
                          "Official engineering blog - payments infra, scaling Postgres, incident postmortems.",
                          "news", "fixture"),
            ]
        else:
            items = [
                IntelItem(f"Fixture result for: {query}",
                          "https://example.com/fixture",
                          "Offline fixture result - no live search performed.",
                          "news", "fixture"),
            ]
        return items[:limit]
