from enum import Enum, unique


@unique
class CurrencyCodes(Enum):
    """
    Currency codes to use around the app.
    Feel free to increase the enum as needed.
    """

    EUR: str = "EUR"

    def __str__(self):
        return self.value
