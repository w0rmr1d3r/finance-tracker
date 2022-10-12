from finance_tracker.money.currency_codes import CurrencyCodes


class CurrencyCodeIsNoneException(Exception):
    pass


class CurrencyIsNotTheSameException(Exception):
    pass


class Money:
    def __init__(self, currency_code: CurrencyCodes, amount: float = 0.0):
        if currency_code is None:
            raise CurrencyCodeIsNoneException()
        self._amount = amount
        self._currency_code = currency_code

    @property
    def amount(self):
        return self._amount

    @property
    def currency_code(self):
        return self._currency_code

    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency_code != self.currency_code:
                raise CurrencyIsNotTheSameException()
            other = other.amount
        amount = self.amount + other
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency_code != self.currency_code:
                raise CurrencyIsNotTheSameException()
            other = other.amount
        amount = self.amount - other
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __eq__(self, other):
        if isinstance(other, Money):
            return (self._amount == other.amount) and (self._currency_code == other.currency_code)
        return False

    def __str__(self):
        rounded_amount = round(self.amount, 2)
        return f"{rounded_amount}{self.currency_code}"


DEFAULT_MONEY = Money(currency_code=CurrencyCodes.EUR)
