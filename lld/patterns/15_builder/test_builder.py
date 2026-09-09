"""Tests for the 15 — Builder demo.

Run:  ./lld/run_tests.sh                          # every LLD test
      .venv/bin/pytest lld/patterns/15_builder -q   # this item alone

pytest puts this folder on sys.path, so `from builder import X` resolves.
"""

import pytest

# from builder import ...


@pytest.mark.skip(reason="not started")
def test_placeholder():
    """Delete this test.

    Write 1 test for each part you named in README section 2.
    If a part needs no test, you probably do not need the part.
    """
    assert False
