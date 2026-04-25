"""Budget enforcement for the ingest pipeline.

Keeps running totals of tokens and $ spent; raises BudgetExceeded if a book
or the batch runs over.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Rough pricing: Minimax M2.7-highspeed (via minimaxi.com) is cheaper than
# Anthropic direct; we use a conservative unified rate for estimation. Adjust
# when the real billing line item is known.
PRICE_PER_MILLION_TOKENS_IN = 2.0
PRICE_PER_MILLION_TOKENS_OUT = 4.0


class BudgetExceeded(Exception):
    """Raised when per-book or batch budget is about to be exceeded."""


@dataclass
class BookSpend:
    book_stem: str
    tokens_in: int = 0
    tokens_out: int = 0
    dollars: float = 0.0
    llm_calls: int = 0


@dataclass
class CostTracker:
    per_book_cap: float = 2.0
    batch_cap: float = 500.0
    books: dict[str, BookSpend] = field(default_factory=dict)
    total_dollars: float = 0.0

    def _book(self, stem: str) -> BookSpend:
        if stem not in self.books:
            self.books[stem] = BookSpend(book_stem=stem)
        return self.books[stem]

    def add_usage(self, book_stem: str, tokens_in: int, tokens_out: int) -> float:
        """Record a single LLM call; returns the $ for this call.

        Raises BudgetExceeded BEFORE recording if the call would push either
        cap over. The caller is therefore expected to have decided the call
        is necessary.
        """
        cost = (
            tokens_in / 1_000_000 * PRICE_PER_MILLION_TOKENS_IN
            + tokens_out / 1_000_000 * PRICE_PER_MILLION_TOKENS_OUT
        )
        book = self._book(book_stem)
        if book.dollars + cost > self.per_book_cap:
            raise BudgetExceeded(
                f"Book '{book_stem}' would exceed per-book cap "
                f"(${self.per_book_cap:.2f}): current ${book.dollars:.2f} + "
                f"this ${cost:.4f}"
            )
        if self.total_dollars + cost > self.batch_cap:
            raise BudgetExceeded(
                f"Batch would exceed batch cap (${self.batch_cap:.2f}): "
                f"current ${self.total_dollars:.2f} + this ${cost:.4f}"
            )
        book.tokens_in += tokens_in
        book.tokens_out += tokens_out
        book.dollars += cost
        book.llm_calls += 1
        self.total_dollars += cost
        return cost

    def summary(self) -> dict:
        return {
            "total_dollars": round(self.total_dollars, 4),
            "batch_cap": self.batch_cap,
            "per_book_cap": self.per_book_cap,
            "books": {k: asdict(v) for k, v in self.books.items()},
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.summary(), indent=2, ensure_ascii=False))
