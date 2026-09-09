"""Tests for the 12 — Composite demo.

Run:  ./lld/run_tests.sh                          # every LLD test
      .venv/bin/pytest lld/patterns/12_composite -q   # this item alone

pytest puts this folder on sys.path, so `from composite import X` resolves.
"""

import pytest

# from composite import ...


@pytest.mark.skip(reason="not started")
def test_placeholder():
    """Delete this test.

    Write 1 test for each part you named in README section 2.
    If a part needs no test, you probably do not need the part.
    """
    assert False
