from enum import Enum, unique


@unique
class CurrencyCodes(Enum):
    EUR: str = "EUR"

    def __str__(self):
        return self.value
