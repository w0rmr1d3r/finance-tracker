import json

from finance_tracker.money.currency_codes import CurrencyCodes


def test_currency_code_is_json_serializable():
    currency_code = CurrencyCodes.EUR
    currency_code_dumped = json.dumps(currency_code)
    currency_code_loaded = json.loads(currency_code_dumped)
    assert currency_code_loaded == currency_code
