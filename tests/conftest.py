from typing import Dict

import pytest


@pytest.fixture
def all_categories() -> Dict:
    return {
        "CATEGORIES": {"PAYCHECK": ["PAYCHECK_FROM_COMPANY"]},
        "POSITIVE_CATEGORIES": [],
    }
