from typing import Any
from interest import compound_interest, base_amount, monthly
class Calculation:
    index_to_function = {
        0: compound_interest,
        1: monthly,
        2: base_amount
    }
    def __init__(self, use_case_index):
        self.calculation_function = self.index_to_function[use_case_index]

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.calculation_function(*args, **kwargs)
