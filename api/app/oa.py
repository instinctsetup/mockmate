"""OA question bank: seeded real problems with source URLs.

Every question links to its public problem page (source). Company tags are
community-reported associations, NOT verified claims - the API and UI say so.
Solutions are model-written and always labeled model_written=True.
"""
from dataclasses import dataclass, field, asdict


@dataclass
class OAQuestion:
    id: str
    title: str
    difficulty: str          # easy | medium | hard
    topics: list[str]
    url: str                 # source: the public problem page
    companies: list[str] = field(default_factory=list)  # community-reported
    solution: str = ""       # model-written, labeled
    model_written: bool = True


# Seed bank. URLs are the canonical public LeetCode problem pages.
# companies: widely community-reported tags (LeetCode's own company tag
# feature surfaces these to subscribers); treated as hints, not facts.
_BANK = [
    OAQuestion("two-sum", "Two Sum", "easy", ["arrays", "hashmap"],
               "https://leetcode.com/problems/two-sum/",
               ["amazon", "google", "razorpay"],
               "Hashmap value->index; one pass. For each x check target-x seen. O(n) time, O(n) space."),
    OAQuestion("lru-cache", "LRU Cache", "medium", ["design", "hashmap", "linked-list"],
               "https://leetcode.com/problems/lru-cache/",
               ["amazon", "microsoft", "razorpay"],
               "Hashmap + doubly-linked list. get/put O(1): map key->node, list ordered by recency."),
    OAQuestion("number-of-islands", "Number of Islands", "medium", ["graphs", "dfs", "bfs"],
               "https://leetcode.com/problems/number-of-islands/",
               ["amazon", "google"],
               "Flood-fill: scan grid, DFS/BFS from each unvisited '1', count components. O(mn)."),
    OAQuestion("merge-intervals", "Merge Intervals", "medium", ["arrays", "sorting"],
               "https://leetcode.com/problems/merge-intervals/",
               ["google", "microsoft", "flipkart"],
               "Sort by start; extend current interval while overlap, else emit. O(n log n)."),
    OAQuestion("binary-tree-level-order", "Binary Tree Level Order Traversal", "medium",
               ["trees", "bfs"], "https://leetcode.com/problems/binary-tree-level-order-traversal/",
               ["amazon", "microsoft"],
               "BFS with queue; snapshot queue size per level. O(n)."),
    OAQuestion("trapping-rain-water", "Trapping Rain Water", "hard", ["arrays", "two-pointers", "dp"],
               "https://leetcode.com/problems/trapping-rain-water/",
               ["google", "amazon"],
               "Two pointers tracking max-left/max-right; add min(maxL,maxR)-h. O(n) time O(1) space."),
    OAQuestion("course-schedule", "Course Schedule", "medium", ["graphs", "topological-sort"],
               "https://leetcode.com/problems/course-schedule/",
               ["amazon", "google", "razorpay"],
               "Cycle detection in directed graph: Kahn's BFS or DFS colors. O(V+E)."),
    OAQuestion("longest-substring-without-repeating", "Longest Substring Without Repeating Characters",
               "medium", ["strings", "sliding-window", "hashmap"],
               "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
               ["amazon", "google"],
               "Sliding window with last-seen index map; move left past duplicate. O(n)."),
    OAQuestion("coin-change", "Coin Change", "medium", ["dp"],
               "https://leetcode.com/problems/coin-change/",
               ["amazon", "razorpay"],
               "DP: dp[a]=min(dp[a-c]+1). O(amount*coins)."),
    OAQuestion("valid-parentheses", "Valid Parentheses", "easy", ["strings", "stack"],
               "https://leetcode.com/problems/valid-parentheses/",
               ["amazon", "microsoft"],
               "Stack: push opens, pop on close and match. O(n)."),
    OAQuestion("kth-largest", "Kth Largest Element in an Array", "medium",
               ["arrays", "heap", "quickselect"], "https://leetcode.com/problems/kth-largest-element-in-an-array/",
               ["amazon", "microsoft", "flipkart"],
               "Quickselect average O(n), or min-heap of size k O(n log k)."),
    OAQuestion("word-break", "Word Break", "medium", ["dp", "strings", "trie"],
               "https://leetcode.com/problems/word-break/",
               ["google", "amazon"],
               "DP over prefixes: dp[i] = any(dp[j] and s[j:i] in dict). O(n^2) with set."),
    OAQuestion("invert-binary-tree", "Invert Binary Tree", "easy", ["trees", "dfs"],
               "https://leetcode.com/problems/invert-binary-tree/",
               ["google"],
               "Recursively swap left/right children. O(n)."),
    OAQuestion("product-of-array-except-self", "Product of Array Except Self", "medium",
               ["arrays", "prefix-sum"], "https://leetcode.com/problems/product-of-array-except-self/",
               ["amazon", "microsoft", "razorpay"],
               "Two passes: prefix products then suffix products, no division. O(n) time O(1) extra."),
    OAQuestion("serialize-deserialize-binary-tree", "Serialize and Deserialize Binary Tree", "hard",
               ["trees", "design", "dfs"], "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/",
               ["amazon", "google"],
               "Preorder with null markers; rebuild with an iterator. O(n) both ways."),
]

BY_ID = {q.id: q for q in _BANK}


def list_questions(topic: str | None = None, difficulty: str | None = None,
                   company: str | None = None) -> list[dict]:
    out = []
    for q in _BANK:
        if topic and topic not in q.topics:
            continue
        if difficulty and q.difficulty != difficulty:
            continue
        if company and company.lower() not in [c.lower() for c in q.companies]:
            continue
        d = asdict(q)
        d.pop("solution")  # list view: no solutions
        out.append(d)
    return out


def get_question(qid: str) -> dict | None:
    q = BY_ID.get(qid)
    if not q:
        return None
    return asdict(q)


def for_company(company: str) -> list[dict]:
    return list_questions(company=company)
