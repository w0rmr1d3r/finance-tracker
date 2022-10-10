from _pytest.python_api import raises
from faker import Faker

from finance_tracker.money.money import CurrencyCodeIsNoneException, CurrencyIsNotTheSameException, Money


def test_can_create_money():
    currency_code = Faker().currency_code()
    money = Money(currency_code=currency_code)
    assert money.amount == 0.0
    assert money.currency_code == currency_code


def test_can_print_money():
    currency_code = Faker().currency_code()
    money = Money(currency_code=currency_code)
    assert money.__str__() == f"0.0{currency_code}"


def test_money_currency_always_upper():
    currency_code = "eur"
    money = Money(currency_code=currency_code)
    assert money.__str__() == "0.0EUR"


def test_money_are_equal():
    currency_code = Faker().currency_code()
    money_one = Money(currency_code=currency_code, amount=1.0)
    money_two = Money(currency_code=currency_code, amount=1.0)
    assert money_one == money_two


def test_money_are_not_equal():
    currency_code_one = Faker().currency_code()
    currency_code_two = Faker().currency_code()
    money_one = Money(currency_code=currency_code_one, amount=2.0)
    money_two = Money(currency_code=currency_code_two, amount=1.0)
    assert money_one != money_two


def test_raise_exception_if_no_currency_code():
    with raises(CurrencyCodeIsNoneException):
        _ = Money(currency_code=None)


def test_can_add_moneys_of_same_currency():
    currency_code = Faker().currency_code()
    money_one = Money(currency_code=currency_code, amount=1.0)
    money_two = Money(currency_code=currency_code, amount=3.0)
    money_three = money_one + money_two
    assert money_three.amount == 4.0
    assert money_three.currency_code == currency_code


def test_cannot_add_moneys_of_different_currency():
    currency_code_one = Faker().currency_code()
    currency_code_two = Faker().currency_code()
    money_one = Money(currency_code=currency_code_one, amount=1.0)
    money_two = Money(currency_code=currency_code_two, amount=3.0)
    with raises(CurrencyIsNotTheSameException):
        _ = money_one + money_two


def test_can_sub_moneys_of_same_currency():
    currency_code = Faker().currency_code()
    money_one = Money(currency_code=currency_code, amount=1.0)
    money_two = Money(currency_code=currency_code, amount=3.0)
    money_three = money_one - money_two
    assert money_three.amount == -2.0
    assert money_three.currency_code == currency_code


def test_cannot_sub_moneys_of_different_currency():
    currency_code_one = Faker().currency_code()
    currency_code_two = Faker().currency_code()
    money_one = Money(currency_code=currency_code_one, amount=1.0)
    money_two = Money(currency_code=currency_code_two, amount=3.0)
    with raises(CurrencyIsNotTheSameException):
        _ = money_one - money_two
