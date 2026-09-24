"""01 — Strategy — minimal demo.

Rules for this file:
  - 40 lines or fewer. This is not an app.
  - No prints. `test_strategy.py` is how you check it.
  - Real names from the shared domain (see lld/README.md section 6),
    never `ConcreteStrategyA`. A fake name hides whether you understood it.
"""

from abc import ABC, abstractmethod


# TODO: write the smallest code that shows the shape of Strategy.

# Context of a cafeteria, we can handle different payment versions
# Since python does not offer us interfaces OOTB, we will use the abc library (abstrace base class)

# first, we define the interface contract
class IPaymentStrategy(ABC):
    @abstractmethod
    def make_payment(self, amount: int) -> None:
        pass


# Credit card payment
class CreditCardPayment(IPaymentStrategy):
    
    def __init__(self, card_number: str) -> None:
        self.card_number =  card_number

    def make_payment(self, amount: int) -> None:
        print(f"Making a {amount} payment with card number: {self.card_number}")


class PayPalPayment(IPaymentStrategy):
    def __init__(self, acct_num: str) -> None:
        self.acct_num = acct_num
    
    def make_payment(self, amount: int) -> None:
        print(f"Making a {amount} payment with {self.acct_num} Paypal account")

class CryptoPayment(IPaymentStrategy):
    def __init__(self, wallet_addr: str) -> None:
        self.wallet_addr = wallet_addr
    
    def make_payment(self, amount: int) -> None:
        print(f"Making a {amount} payment with {self.wallet_addr} Cyrpto acct")