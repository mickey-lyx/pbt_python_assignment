import importlib.util
from hypothesis import example, given, settings, Verbosity
import hypothesis.strategies as st
import pytest
from datetime import datetime

# Path to the .pyc file
pyc_path = "./__encoded_files__/q2.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

@given(st.text())
@example("31-12-2024")
@example("2024/12/31")
@example("12/31/24")
@example("13/01/2024")
@example("02/30/2024")
@example("02/29/2020")
@example("02/29/2021")
@example("01/01/0001")
@example("12/31/9999")
def test_invalid_input(date_str):
    try:
        date = datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError: # invalid date_str
        # if the date is not valid, the function should raise a ValueError
        try:
            module.parse_date(date_str)
        except ValueError:
            assert True
        else:
            assert False
    else: # valid date_str
        # if the generated date_str happens to be valid, the function should return a datetime that is the same as the input date
        parsed_date = module.parse_date(date_str)
        assert parsed_date == date


@given(st.dates())
def test_parse_valid_date(date):
    input_date = date.strftime("%m/%d/%Y")
    assert module.parse_date(input_date) == date
