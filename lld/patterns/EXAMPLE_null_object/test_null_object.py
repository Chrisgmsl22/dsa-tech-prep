"""Tests for the EXAMPLE — Null Object demo.

Run:  ./lld/run_tests.sh                                    # every LLD test
      .venv/bin/pytest lld/patterns/EXAMPLE_null_object -q   # this item alone

pytest puts this folder on sys.path, so `from null_object import X` resolves.
"""

from null_object import NoPrinter, ThermalPrinter, Till


def test_real_printer_gets_the_receipt():
    printer = ThermalPrinter()
    Till(printer).close_order("A-17", 4.5)
    assert printer.printed == ["A-17 $4.50"]


def test_null_printer_is_silent_and_does_not_crash():
    printer = NoPrinter()
    total = Till(printer).close_order("A-18", 3.25)
    assert total == 3.25


def test_the_till_treats_both_printers_the_same():
    """The point of the pattern: 1 code path, no None check."""
    for printer in (ThermalPrinter(), NoPrinter()):
        assert Till(printer).close_order("A-19", 2.0) == 2.0
