"""L3: gate checks and cost tracker — they do not exercise the LLM."""
from __future__ import annotations

import pytest

from scripts.ingest.cost_tracker import BudgetExceeded, CostTracker
from scripts.ingest.validate import (
    check_approval_gate_required,
    check_file_count_threshold,
)


# ---------- file-count gate ----------


def test_under_limit_no_error() -> None:
    assert check_file_count_threshold(["a.md"] * 9) == []


def test_exactly_at_limit_no_error() -> None:
    assert check_file_count_threshold(["a.md"] * 10) == []


def test_over_limit_error() -> None:
    errs = check_file_count_threshold(["a.md"] * 11)
    assert errs and "requires explicit batch approval" in str(errs[0])


def test_over_limit_with_approval_ok() -> None:
    assert check_file_count_threshold(["a.md"] * 50, approved_batch=True) == []


# ---------- approval gate ----------


def test_all_high_risk_blocked_without_approval() -> None:
    for action in ("delete", "merge", "rename", "schema_edit", "collapse_conflict"):
        assert check_approval_gate_required(action) != [], action


def test_all_high_risk_allowed_with_approval() -> None:
    for action in ("delete", "merge", "rename", "schema_edit", "collapse_conflict"):
        assert check_approval_gate_required(action, approved=True) == [], action


def test_low_risk_actions_pass_through() -> None:
    for action in ("create", "update", "append", "link"):
        assert check_approval_gate_required(action) == [], action


# ---------- cost tracker ----------


def test_cost_tracker_records_usage() -> None:
    ct = CostTracker(per_book_cap=1.0, batch_cap=10.0)
    spent = ct.add_usage("book-a", tokens_in=10_000, tokens_out=2_000)
    assert 0 < spent < 1.0
    assert ct.total_dollars == pytest.approx(spent)
    assert ct.books["book-a"].llm_calls == 1


def test_cost_tracker_per_book_cap_enforced() -> None:
    ct = CostTracker(per_book_cap=0.05, batch_cap=100.0)
    ct.add_usage("book-a", tokens_in=10_000, tokens_out=2_000)
    with pytest.raises(BudgetExceeded):
        ct.add_usage("book-a", tokens_in=500_000, tokens_out=500_000)


def test_cost_tracker_batch_cap_enforced() -> None:
    ct = CostTracker(per_book_cap=100.0, batch_cap=0.05)
    with pytest.raises(BudgetExceeded):
        ct.add_usage("book-a", tokens_in=500_000, tokens_out=500_000)


def test_cost_tracker_summary_has_books() -> None:
    ct = CostTracker(per_book_cap=1.0, batch_cap=10.0)
    ct.add_usage("book-a", 1000, 500)
    ct.add_usage("book-b", 2000, 800)
    summary = ct.summary()
    assert summary["total_dollars"] > 0
    assert set(summary["books"].keys()) == {"book-a", "book-b"}
