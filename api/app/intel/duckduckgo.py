"""Live search via DuckDuckGo's public HTML endpoint.

No login, no API key, no scraping of login-walled sites. Results link out to
the original pages; we store only title/URL/snippet.
"""
import urllib.parse
import urllib.request
import re
from .base import IntelItem, SearchProvider

_UA = {"User-Agent": "mockmate/1.0 (+https://github.com/instinctsetup/mockmate)"}


class DuckDuckGoProvider(SearchProvider):
    name = "duckduckgo"

    def search(self, query: str, limit: int = 10) -> list[IntelItem]:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers=_UA)
        try:
            html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "replace")
        except Exception:
            return []
        items = []
        links = re.findall(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.S)
        for i, (href, title) in enumerate(links[:limit]):
            m = re.search(r"uddg=([^&]+)", href)
            real = urllib.parse.unquote(m.group(1)) if m else href
            clean = lambda s: re.sub(r"<[^>]+>", "", s).strip()
            snip = clean(snippets[i]) if i < len(snippets) else ""
            items.append(IntelItem(clean(title), real, snip, "news", self.name))
        return items
