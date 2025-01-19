import importlib.util
from hypothesis import given, example, settings
import hypothesis.strategies as st
import pytest

# Path to the .pyc file
pyc_path = "./__encoded_files__/q3.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

@pytest.mark.timeout(5, method="thread")
@given(st.lists(st.integers()).map(sorted), st.integers())
@settings(deadline=1000)
# Empty list test
@example([], 1)
# Single element list tests
@example([1], 1)  # Element exists
@example([1], 2)  # Element doesn't exist
# Two elements list tests
@example([1, 2], 1)  # Search first element
@example([1, 2], 2)  # Search last element
@example([1, 2], 0)  # Search element less than minimum
@example([1, 2], 3)  # Search element greater than maximum
# Odd length list test
@example([1, 3, 5], 3)  # Search middle element
# Even length list tests
@example([1, 2, 3, 4], 2)  # Search in left half
@example([1, 2, 3, 4], 3)  # Search in right half
# Duplicate elements test
@example([1, 1, 1], 1)
# Negative numbers test
@example([-2, 0, 2], -2)  # Search negative number
@example([-2, 0, 2], 0)   # Search zero
# Large numbers test
@example([-1000000, 0, 1000000], 1000000)
def test_binary_search(list, target):
    index = module.binary_search(list, target)
    if target in list:
        assert 0 <= index < len(list)
        assert list[index] == target
    else:
        assert index == -1

