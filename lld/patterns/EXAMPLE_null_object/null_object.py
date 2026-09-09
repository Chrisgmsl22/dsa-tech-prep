"""EXAMPLE — Null Object — minimal demo.

Rules for this file:
  - 40 lines or fewer. This is not an app.
  - No prints. `test_null_object.py` is how you check it.
  - Real names from the shared domain (see lld/README.md section 6).
"""

from abc import ABC, abstractmethod


class Printer(ABC):
    """What the till is allowed to ask a printer to do."""

    @abstractmethod
    def print_receipt(self, order_id: str, total: float) -> None:
        raise NotImplementedError


class ThermalPrinter(Printer):
    """The real printer. It keeps a log, because a test cannot read paper."""

    def __init__(self) -> None:
        self.printed: list[str] = []

    def print_receipt(self, order_id: str, total: float) -> None:
        self.printed.append(f"{order_id} ${total:.2f}")


class NoPrinter(Printer):
    """The null object: a full member of the interface that does nothing."""

    def print_receipt(self, order_id: str, total: float) -> None:
        return None


class Till:
    def __init__(self, printer: Printer) -> None:
        self.printer = printer

    def close_order(self, order_id: str, total: float) -> float:
        self.printer.print_receipt(order_id, total)  # never `if self.printer:`
        return total
