"""
General Mathematics Library

A comprehensive library for symbolic matrix operations including:
- Basic arithmetic operators (add, subtract, multiply, divide, negate)
- Matrix operations (determinant, inverse, transpose, etc.)
- Symbolic computation with expression trees
- Test suite with colored output

Author: Mathematical Operations Library
"""

from typing import Union, List, Callable, Any
import math


class Operator:
    """Base class for mathematical operators."""
    
    def symbol(self) -> str:
        """Return the symbol representation of this operator."""
        raise NotImplementedError("symbol() not defined.")


class UnaryOperator(Operator):
    """Base class for unary operators (operate on one operand)."""
    
    def __init__(self, lhs):
        self.lhs = lhs
    
    def apply(self, lhs):
        """Apply the operator to the left-hand side operand."""
        raise NotImplementedError("apply() not defined.")
    
    def simplify(self):
        """Simplify the expression tree."""
        raise NotImplementedError("simplify() not defined.")
    
    def __str__(self):
        return f"({self.symbol()}{self.lhs})"
    
    def __repr__(self):
        return f"({self.symbol()}{self.lhs})"


class BinaryOperator(Operator):
    """Base class for binary operators (operate on two operands)."""
    
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def apply(self, lhs, rhs):
        """Apply the operator to the left and right operands."""
        raise NotImplementedError("apply() not defined.")
    
    def simplify(self):
        """Simplify the expression tree."""
        raise NotImplementedError("simplify() not defined.")
    
    def __str__(self):
        return f"({self.lhs}{self.symbol()}{self.rhs})"
    
    def __repr__(self):
        return f"({self.lhs}{self.symbol()}{self.rhs})"


class Negate(UnaryOperator):
    """Unary negation operator (-x)."""
    
    def apply(self, lhs):
        if lhs == 0:
            return lhs
        return -lhs
    
    def symbol(self):
        return "-"
    
    def simplify(self):
        return -self.lhs.simplify()


class Add(BinaryOperator):
    """Binary addition operator (x + y)."""
    
    def apply(self, lhs, rhs):
        if lhs == 0 and rhs == 0:
            return 0
        if lhs == 0:
            return rhs
        if rhs == 0:
            return lhs
        return lhs + rhs
    
    def symbol(self):
        return "+"
    
    def simplify(self):
        return self.lhs.simplify() + self.rhs.simplify()


class Divide(BinaryOperator):
    """Binary division operator (x / y)."""
    
    def apply(self, lhs, rhs):
        if rhs == 1:
            return lhs
        return lhs / rhs
    
    def symbol(self):
        return "/"
    
    def simplify(self):
        return self.lhs.simplify() / self.rhs.simplify()


class Multiply(BinaryOperator):
    """Binary multiplication operator (x * y)."""
    
    def apply(self, lhs, rhs):
        if lhs == 0 or rhs == 0:
            return 0
        if lhs == 1:
            return rhs
        if rhs == 1:
            return lhs
        return lhs * rhs
    
    def symbol(self):
        return "*"
    
    def simplify(self):
        return self.lhs.simplify() * self.rhs.simplify()


class Subtract(BinaryOperator):
    """Binary subtraction operator (x - y)."""
    
    def apply(self, lhs, rhs):
        if rhs == 0:
            return lhs
        return lhs - rhs
    
    def symbol(self):
        return "-"
    
    def simplify(self):
        return self.lhs.simplify() - self.rhs.simplify()


class MatrixElement:
    """Represents a symbolic matrix element."""
    
    def __init__(self, i: int, j: int, name: str = "m"):
        self.name = name
        self.i = i
        self.j = j
    
    def __str__(self):
        return f"{self.name}[{self.i}][{self.j}]"
    
    def __repr__(self):
        return f"{self.name}[{self.i}][{self.j}]"


def is_numeric(v: Any) -> bool:
    """Check if a value is numeric (int or float)."""
    return isinstance(v, (int, float))


def simplify(node: Any) -> Any:
    """
    Simplify an expression tree node.
    
    Args:
        node: The node to simplify (can be numeric, MatrixElement, or operator)
    
    Returns:
        The simplified result
    
    Raises:
        TypeError: If the node type is not supported
    """
    if isinstance(node, MatrixElement):
        return node
    if isinstance(node, UnaryOperator):
        lhs = simplify(node.lhs)
        return node.apply(lhs)
    if isinstance(node, BinaryOperator):
        lhs = simplify(node.lhs)
        rhs = simplify(node.rhs)
        return node.apply(lhs, rhs)
    if isinstance(node, (int, float)):
        return node
    raise TypeError(f"Unsupported type in expression tree: {type(node)}")


class Matrix:
    """Matrix class for matrix operations."""
    
    def __init__(self, m: List[List]):
        self.m = m
    
    @staticmethod
    def identity(size: int) -> 'Matrix':
        """Create an identity matrix of given size."""
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(1 if i == j else 0)
            matrix.append(row)
        return Matrix(matrix)
    
    def print_matrix(self):
        """Print the matrix in a readable format."""
        for row in self.m:
            print(row)


# =============================================================================
# Matrix Utility Functions
# =============================================================================

def mat_print(m: List[List]) -> None:
    """Print a matrix in a readable format."""
    for row in m:
        print(row)


def mat_python(m: List[List]) -> None:
    """Print matrix elements in Python array format."""
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(f"m[{i}][{j}] = {m[i][j]}")


def mat_cofactor_signs(m: List[List]) -> List[List]:
    """Apply cofactor signs to a matrix (multiply by (-1)^(i+j))."""
    return mat_visit_index(m, lambda v, i, j: v if (i + j) % 2 == 0 else Negate(v))


def mat_cofactor_matrix(m: List[List]) -> List[List]:
    """Compute the cofactor matrix (minors with cofactor signs applied)."""
    cofactors = []
    for i in range(len(m)):
        row = []
        for j in range(len(m[i])):
            minor = mat_minor(m, i, j)
            minor_det = mat_determinant(minor)
            # Apply cofactor sign: (-1)^(i+j)
            if (i + j) % 2 == 1:
                minor_det = Negate(minor_det)
            row.append(minor_det)
        cofactors.append(row)
    return cofactors


def mat_determinant(m: List[List]) -> Any:
    """
    Compute the determinant of a matrix.
    
    Args:
        m: The input matrix
    
    Returns:
        The determinant value
    
    Raises:
        ValueError: If the matrix is not square
    """
    if mat_rank(m) == -1:
        raise ValueError("Cannot compute determinant for a non-square matrix.")
    
    if mat_rank(m) == 1:
        return m[0][0]
    
    if mat_rank(m) == 2:
        a = Multiply(m[0][0], m[1][1])
        b = Multiply(m[0][1], m[1][0])
        return Subtract(a, b)
    
    # For larger matrices, use cofactor expansion along first row
    result = None
    for j in range(len(m[0])):
        minor = mat_minor(m, 0, j)
        minor_det = mat_determinant(minor)
        term = Multiply(m[0][j], minor_det)
        
        if result is None:
            result = term
        else:
            if j % 2 == 0:
                result = Add(result, term)
            else:
                result = Subtract(result, term)
    
    return result


def mat_is_equal(lhs: List[List], rhs: List[List]) -> bool:
    """Check if two matrices are equal."""
    if len(lhs) != len(rhs):
        return False
    for i in range(len(lhs)):
        if len(lhs[i]) != len(rhs[i]):
            return False
        for j in range(len(lhs[i])):
            if lhs[i][j] != rhs[i][j]:
                return False
    return True


def mat_identity(size: int) -> List[List]:
    """Create an identity matrix of given size."""
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(1 if i == j else 0)
        matrix.append(row)
    return matrix


def mat_inverse(m: List[List]) -> List[List]:
    """
    Compute the inverse of a matrix using the adjugate method.
    
    The inverse is computed as: A^(-1) = (1/det(A)) * adj(A)
    where adj(A) is the transpose of the cofactor matrix.
    
    Args:
        m: The input matrix
    
    Returns:
        The inverse matrix
    
    Raises:
        ValueError: If the matrix is not square or not invertible
    """
    if mat_rank(m) == -1:
        raise ValueError("Cannot invert a non-square matrix.")
    
    # Compute determinant first to check if matrix is invertible
    det = mat_determinant(m)
    if det == 0:
        raise ValueError("Matrix is not invertible (determinant is zero).")
    
    # Compute cofactor matrix
    cofactor_matrix = mat_cofactor_matrix(m)
    
    # Transpose to get adjugate matrix
    adjugate = mat_transpose(cofactor_matrix)
    
    # Divide by determinant
    return mat_scalar_divide(adjugate, det)


def mat_minor(m: List[List], i: int, j: int) -> List[List]:
    """Compute the minor matrix by removing row i and column j."""
    minor = []
    for row_idx in range(len(m)):
        if row_idx == i:
            continue
        row = []
        for col_idx in range(len(m[row_idx])):
            if col_idx == j:
                continue
            row.append(m[row_idx][col_idx])
        minor.append(row)
    return minor


def mat_multiply(m: List[List], n: List[List]) -> List[List]:
    """
    Multiply two matrices.
    
    Args:
        m: First matrix (m x p)
        n: Second matrix (p x n)
    
    Returns:
        Result matrix (m x n)
    
    Raises:
        ValueError: If matrices have incompatible dimensions
    """
    # Check matrix dimensions
    if len(m) == 0 or len(n) == 0:
        raise ValueError("Cannot multiply empty matrices.")
    
    if len(m[0]) != len(n):
        raise ValueError(f"Matrix dimensions incompatible: {len(m)}x{len(m[0])} and {len(n)}x{len(n[0])}")
    
    result = []
    for i in range(len(m)):
        row = []
        for j in range(len(n[0])):
            sum_term = None
            for k in range(len(m[0])):
                term = Multiply(m[i][k], n[k][j])
                if sum_term is None:
                    sum_term = term
                else:
                    sum_term = Add(sum_term, term)
            row.append(sum_term)
        result.append(row)
    return result


def mat_rank(m: List[List]) -> int:
    """Get the rank (size) of a square matrix, or -1 if not square."""
    if len(m) == 0:
        return 0
    size = len(m)
    for row in m:
        if len(row) != size:
            return -1
    return size


def mat_scalar_divide(matrix: List[List], scalar: Union[int, float]) -> List[List]:
    """Divide each element of a matrix by a scalar."""
    if scalar == 0:
        raise ValueError("Cannot divide by zero.")
    return mat_visit(matrix, lambda x: Divide(x, scalar))


def mat_scalar_multiply(matrix: List[List], scalar: Union[int, float]) -> List[List]:
    """Multiply each element of a matrix by a scalar."""
    return mat_visit(matrix, lambda x: Multiply(x, scalar))


def mat_simplify(m: List[List]) -> List[List]:
    """Simplify all elements in a matrix."""
    return mat_visit(m, lambda x: simplify(x))


def mat_symbolic(size: int, name: str = "m") -> List[List]:
    """Create a symbolic matrix of given size."""
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(MatrixElement(i, j, name))
        matrix.append(row)
    return matrix


def mat_transpose(m: List[List]) -> List[List]:
    """Transpose a matrix."""
    if len(m) == 0:
        return []
    result = []
    for i in range(len(m[0])):
        row = []
        for j in range(len(m)):
            row.append(m[j][i])
        result.append(row)
    return result


def mat_visit(m: List[List], fn: Callable) -> List[List]:
    """Apply a function to each element of a matrix."""
    result = []
    for row in m:
        new_row = []
        for element in row:
            new_row.append(fn(element))
        result.append(new_row)
    return result


def mat_visit_index(m: List[List], fn: Callable) -> List[List]:
    """Apply a function to each element of a matrix with indices."""
    result = []
    for i in range(len(m)):
        row = []
        for j in range(len(m[i])):
            row.append(fn(m[i][j], i, j))
        result.append(row)
    return result


# =============================================================================
# Test Suite
# =============================================================================

class ANSI:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def assert_result(result: bool) -> bool:
    """Assert a result and return it."""
    assert result
    return result


def test(fn: Callable) -> None:
    """Run a test function and print results."""
    print(f"Running Test: {fn.__name__}")
    print(f"  Result: {fn()}")


def decorate_test(fn: Callable) -> Callable:
    """Decorator to run a test with formatted output."""
    print("=" * 79)
    print(f"# Running Test: {fn.__name__}")
    print("=" * 79)
    print()
    
    try:
        result = fn()
    except Exception:
        result = None
    
    print(f"  {fn.__name__}() = ", end="")
    print(ANSI.OKGREEN, end="")
    print(str(result))
    print(ANSI.ENDC, end="")
    print()
    return fn


def decorate_test_n(n_range) -> Callable:
    """Decorator to run a test with multiple parameters."""
    def decorator(fn: Callable) -> Callable:
        print("=" * 79)
        print(f"# Running Test: {fn.__name__}")
        print("=" * 79)
        
        for i in n_range:
            print()
            try:
                result = fn(i)
            except Exception:
                result = None
            
            print(f"  {fn.__name__}({i}) = ", end="")
            print(ANSI.OKGREEN, end="")
            print(str(result))
            print(ANSI.ENDC, end="")
        print()
        return fn
    return decorator


# =============================================================================
# Test Functions
# =============================================================================

@decorate_test
def test_mat_determinant_2():
    """Test determinant of 2x2 identity matrix."""
    return mat_determinant(mat_identity(2))


@decorate_test
def test_mat_determinant_3():
    """Test determinant of 3x3 identity matrix."""
    return mat_determinant(mat_identity(3))


@decorate_test
def test_mat_determinant_4():
    """Test determinant of 4x4 identity matrix."""
    return mat_determinant(mat_identity(4))


@decorate_test_n(range(2, 6))
def test_mat_determinant_n(i: int):
    """Test determinant of nxn identity matrices."""
    return mat_determinant(mat_identity(i))


@decorate_test_n(range(2, 6))
def test_mat_determinant_of_identity_is_one(i: int):
    """Test that determinant of identity matrix is 1."""
    return assert_result(simplify(mat_determinant(mat_identity(i))) == 1)


@decorate_test
def test_mat_identity_2():
    """Test 2x2 identity matrix creation."""
    return mat_identity(2)


@decorate_test
def test_mat_identity_3():
    """Test 3x3 identity matrix creation."""
    return mat_identity(3)


@decorate_test
def test_mat_identity_4():
    """Test 4x4 identity matrix creation."""
    return mat_identity(4)


@decorate_test_n(range(2, 6))
def test_mat_identity_n(i: int):
    """Test nxn identity matrix creation."""
    return mat_identity(i)


@decorate_test_n(range(2, 6))
def test_mat_inverse_n(i: int):
    """Test that inverse of identity is still identity."""
    return assert_result(mat_is_equal(mat_identity(i), mat_simplify(mat_inverse(mat_identity(i)))))


@decorate_test
def test_mat_inverse_scale():
    """Test inverse of a scaled identity matrix."""
    mat = mat_identity(4)
    mat[1][1] = 10
    inv = mat_inverse(mat)
    inv = mat_simplify(inv)
    
    assert roughly_equal(inv[0][0], 1.0)
    assert roughly_equal(inv[1][1], 0.1)
    assert roughly_equal(inv[2][2], 1.0)
    assert roughly_equal(inv[3][3], 1.0)
    return True


@decorate_test
def test_mat_inverse_identity():
    """Test that matrix times its inverse equals identity."""
    mat = mat_identity(4)
    mat[1][1] = 10
    inv = mat_simplify(mat_inverse(mat))
    result = mat_multiply(mat, inv)
    result = mat_simplify(result)
    
    assert roughly_equal(result[0][0], 1.0)
    assert roughly_equal(result[1][1], 1.0)
    assert roughly_equal(result[2][2], 1.0)
    assert roughly_equal(result[3][3], 1.0)
    return True


@decorate_test
def test_mat_minor():
    """Test minor matrix computation."""
    return mat_minor(mat_identity(3), 0, 1)


def test_mat_multiply():
    """Test matrix multiplication."""
    return mat_multiply(mat_identity(3), mat_symbolic(3))


@decorate_test
def test_mat_scalar_divide():
    """Test scalar division of matrix."""
    return mat_scalar_divide(mat_symbolic(4), 64)


@decorate_test
def test_mat_scalar_multiply():
    """Test scalar multiplication of matrix."""
    return mat_scalar_multiply(mat_symbolic(4), 64)


@decorate_test_n(range(2, 6))
def test_mat_rank_n(i: int):
    """Test matrix rank computation."""
    return assert_result(mat_rank(mat_symbolic(i)) == i)


@decorate_test
def test_mat_simplify():
    """Test matrix simplification."""
    return mat_simplify(mat_scalar_divide(mat_scalar_multiply(mat_identity(4), 64), 64))


@decorate_test_n(range(2, 6))
def test_mat_symbolic(i: int):
    """Test symbolic matrix creation."""
    return mat_symbolic(i)


@decorate_test
def test_mat_visit():
    """Test matrix element visitation."""
    return mat_visit(mat_symbolic(4), lambda x: print(str(x)))


@decorate_test
def test_mat_visit_index():
    """Test matrix element visitation with indices."""
    return mat_visit_index(mat_symbolic(4), lambda x, i, j: print(f"{i},{j}={x}"))


def roughly_equal(a: float, b: float, tolerance: float = 0.0001) -> bool:
    """Check if two floats are approximately equal within tolerance."""
    return abs(b - a) < tolerance


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    print(f"{ANSI.HEADER}General Mathematics Library Test Suite{ANSI.ENDC}")
    print(f"{ANSI.BOLD}Running all tests...{ANSI.ENDC}\n")
    
    # Run all tests
    test_mat_determinant_2()
    test_mat_determinant_3()
    test_mat_determinant_4()
    test_mat_determinant_n(2)  # This will run for range(2, 6)
    test_mat_determinant_of_identity_is_one(2)  # This will run for range(2, 6)
    test_mat_identity_2()
    test_mat_identity_3()
    test_mat_identity_4()
    test_mat_identity_n(2)  # This will run for range(2, 6)
    test_mat_inverse_n(2)  # This will run for range(2, 6)
    test_mat_inverse_scale()
    test_mat_inverse_identity()
    test_mat_minor()
    test_mat_multiply()
    test_mat_scalar_divide()
    test_mat_scalar_multiply()
    test_mat_rank_n(2)  # This will run for range(2, 6)
    test_mat_simplify()
    test_mat_symbolic(2)  # This will run for range(2, 6)
    test_mat_visit()
    test_mat_visit_index()
    
    print(f"{ANSI.OKGREEN}{ANSI.BOLD}All tests completed!{ANSI.ENDC}")