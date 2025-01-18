import hypothesis.strategies as st
from hypothesis import given, assume, example
import importlib.util
import pytest
# Path to the .pyc file
pyc_path = "./__encoded_files__/q1.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
print(spec)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

@given(st.lists(st.lists(st.integers())))
def test_invalid_input(matrix):
    assume(len(matrix) > 0)
    assume(any(len(row) != len(matrix[0]) for row in matrix))
    with pytest.raises(ValueError):
        module.transpose(matrix)

@given(st.lists(st.lists(st.integers())))
@example([[]])
@example([[1], [2], [3]])
@example([[1, 2, 3]])
@example([[1, 2], [3, 4], [5, 6]])
@example([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
@example([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
@example([[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]])
def test_transpose(matrix):
    # make sure all rows have the same length
    assume(all(len(row) == len(matrix[0]) for row in matrix))

    # transpose the matrix
    transposed = module.transpose(matrix)

    # check the dimensions of the transposed matrix
    assert len(transposed) == len(matrix[0])  # the number of columns becomes the number of rows
    assert all(len(row) == len(matrix) for row in transposed)  # the number of rows becomes the number of columns

    # check if the elements are correctly transposed
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            assert transposed[j][i] == matrix[i][j]

@given(st.lists(st.lists(st.integers())))
def test_transponse_twice(matrix):
    assume(len(matrix) > 0)
    if matrix:
        row_length = len(matrix[0])
        assume(all(len(row) == row_length for row in matrix))
    assert module.transpose(module.transpose(matrix)) == matrix
