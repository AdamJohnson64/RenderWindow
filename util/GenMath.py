"""
General Mathematics Library

A comprehensive library for symbolic matrix operations including:
- Basic arithmetic operators (add, subtract, multiply, divide, negate)
- Matrix operations (determinant, inverse, transpose, etc.)
- Symbolic computation with expression trees
- Test suite with colored output

Author: Mathematical Operations Library
"""

import math
import operator
from typing import Any, Callable, List, Protocol, Union, runtime_checkable


# =============================================================================
# Algebraic Property Protocols
# =============================================================================


@runtime_checkable
class HasIdentity(Protocol):
    """Protocol for operators that have an identity element."""

    @property
    def has_identity(self) -> bool: ...

    @property
    def identity_element(self): ...


@runtime_checkable
class HasZeroElement(Protocol):
    """Protocol for operators that have a zero element."""

    @property
    def has_zero_element(self) -> bool: ...

    @property
    def zero_element(self): ...


@runtime_checkable
class IsCommutative(Protocol):
    """Protocol for commutative operators."""

    @property
    def is_commutative(self) -> bool: ...


@runtime_checkable
class IsAssociative(Protocol):
    """Protocol for associative operators."""

    @property
    def is_associative(self) -> bool: ...


@runtime_checkable
class IsAdditionLike(Protocol):
    """Protocol for operators that behave like addition for zero elements."""

    @property
    def is_addition_like(self) -> bool: ...


@runtime_checkable
class HasOperatorFunction(Protocol):
    """Protocol for operators that have a Python operator function."""

    @property
    def op_func(self): ...


class Operator:
    """Base class for mathematical operators."""

    def symbol(self) -> str:
        """Return the symbol representation of this operator."""
        raise NotImplementedError("symbol() not defined.")

    @property
    def is_associative(self) -> bool:
        """Return True if this operator is associative."""
        return False

    @property
    def is_commutative(self) -> bool:
        """Return True if this operator is commutative."""
        return False

    @property
    def has_identity(self) -> bool:
        """Return True if this operator has an identity element."""
        return False

    @property
    def identity_element(self):
        """Return the identity element for this operator."""
        raise NotImplementedError("identity_element not defined.")

    @property
    def has_zero_element(self) -> bool:
        """Return True if this operator has a zero element."""
        return False

    @property
    def zero_element(self):
        """Return the zero element for this operator."""
        raise NotImplementedError("zero_element not defined.")

    @property
    def is_addition_like(self) -> bool:
        """Return True if this operator behaves like addition for zero elements."""
        return False

    def create_instance(self, *operands):
        """Create a new instance of this operator type with the given operands."""
        raise NotImplementedError("create_instance() not defined.")


class UnaryOperator(Operator):
    """Base class for unary operators (operate on one operand)."""

    def __init__(self, lhs):
        self.lhs = lhs

    def __str__(self):
        return f"({self.symbol()}{self.lhs})"

    def __repr__(self):
        return f"({self.symbol()}{self.lhs})"

    def create_instance(self, operand):
        """Create a new instance of this operator type with the given operand."""
        return type(self)(operand)


class BinaryOperator(Operator):
    """Base class for binary operators (operate on two operands)."""

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"({self.lhs}{self.symbol()}{self.rhs})"

    def __repr__(self):
        return f"({self.lhs}{self.symbol()}{self.rhs})"

    def create_instance(self, lhs, rhs):
        """Create a new instance of this operator type with the given operands."""
        return type(self)(lhs, rhs)


class Negate(UnaryOperator, HasIdentity, HasOperatorFunction):
    """Unary negation operator (-x)."""

    def symbol(self):
        return "-"

    @property
    def has_identity(self) -> bool:
        return True

    @property
    def identity_element(self):
        return 0

    @property
    def op_func(self):
        """Return the Python operator function for this operator."""
        return operator.neg


class Add(BinaryOperator, IsAssociative, IsCommutative, HasIdentity, HasZeroElement, IsAdditionLike, HasOperatorFunction):
    """Binary addition operator (x + y)."""

    def symbol(self):
        return "+"

    @property
    def is_associative(self) -> bool:
        return True

    @property
    def is_commutative(self) -> bool:
        return True

    @property
    def has_identity(self) -> bool:
        return True

    @property
    def identity_element(self):
        return 0

    @property
    def has_zero_element(self) -> bool:
        return True

    @property
    def zero_element(self):
        return 0

    @property
    def is_addition_like(self) -> bool:
        return True

    @property
    def op_func(self):
        """Return the Python operator function for this operator."""
        return operator.add


class Divide(BinaryOperator, HasIdentity, HasOperatorFunction):
    """Binary division operator (x / y)."""

    def symbol(self):
        return "/"

    @property
    def has_identity(self) -> bool:
        return True

    @property
    def identity_element(self):
        return 1

    @property
    def op_func(self):
        """Return the Python operator function for this operator."""
        return operator.truediv


class Multiply(BinaryOperator, IsAssociative, IsCommutative, HasIdentity, HasZeroElement, HasOperatorFunction):
    """Binary multiplication operator (x * y)."""

    def symbol(self):
        return "*"

    @property
    def is_associative(self) -> bool:
        return True

    @property
    def is_commutative(self) -> bool:
        return True

    @property
    def has_identity(self) -> bool:
        return True

    @property
    def identity_element(self):
        return 1

    @property
    def has_zero_element(self) -> bool:
        return True

    @property
    def zero_element(self):
        return 0

    @property
    def is_addition_like(self) -> bool:
        return False

    @property
    def op_func(self):
        """Return the Python operator function for this operator."""
        return operator.mul


class Subtract(BinaryOperator, HasIdentity, HasOperatorFunction):
    """Binary subtraction operator (x - y)."""

    def symbol(self):
        return "-"

    @property
    def has_identity(self) -> bool:
        return True

    @property
    def identity_element(self):
        return 0

    @property
    def op_func(self):
        """Return the Python operator function for this operator."""
        return operator.sub


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


# =============================================================================
# Simplification-Related Functions (lexicographically ordered)
# =============================================================================


def _apply_associative_simplifications(node: BinaryOperator) -> Any:
    """Apply associative simplifications."""
    if not isinstance(node, IsAssociative) or not node.is_associative:
        return node

    # Check if we have nested operators of the same type
    if isinstance(node.lhs, type(node)):
        # (A op const1) op const2 -> A op (const1 op const2)
        if (isinstance(node.lhs.rhs, (int, float)) and
                isinstance(node.rhs, (int, float))):
            if isinstance(node, HasOperatorFunction):
                new_const = node.op_func(node.lhs.rhs, node.rhs)
                return node.create_instance(node.lhs.lhs, new_const)
            else:
                raise ValueError(
                    f"Operator {type(node)} does not have an operator function")

        # (const1 op A) op const2 -> A op (const1 op const2)
        if (isinstance(node.lhs.lhs, (int, float)) and
                isinstance(node.rhs, (int, float))):
            if isinstance(node, HasOperatorFunction):
                new_const = node.op_func(node.lhs.lhs, node.rhs)
                return node.create_instance(node.lhs.rhs, new_const)
            else:
                raise ValueError(
                    f"Operator {type(node)} does not have an operator function")

    # Also check if we have nested operators on the right side
    if isinstance(node.rhs, type(node)):
        # const1 op (const2 op A) -> (const1 op const2) op A
        if (isinstance(node.lhs, (int, float)) and
                isinstance(node.rhs.lhs, (int, float))):
            if isinstance(node, HasOperatorFunction):
                new_const = node.op_func(node.lhs, node.rhs.lhs)
                return node.create_instance(new_const, node.rhs.rhs)
            else:
                raise ValueError(
                    f"Operator {type(node)} does not have an operator function")

        # A op (const1 op B) -> (A op const1) op B
        if isinstance(node.rhs.lhs, (int, float)):
            if isinstance(node, HasOperatorFunction):
                new_lhs = node.create_instance(node.lhs, node.rhs.lhs)
                return node.create_instance(new_lhs, node.rhs.rhs)
            else:
                raise ValueError(
                    f"Operator {type(node)} does not have an operator function")

    return node


def _apply_binary_numeric(operator: BinaryOperator, lhs: Union[int, float],
                         rhs: Union[int, float]) -> Union[int, float]:
    """Apply a binary operator to numeric operands using Python's operator module."""
    # Apply identity and zero simplifications first
    if isinstance(operator, HasIdentity) and operator.has_identity:
        if (isinstance(operator, IsCommutative) and operator.is_commutative and
                (lhs == operator.identity_element or rhs == operator.identity_element)):
            return lhs if rhs == operator.identity_element else rhs
        elif (not isinstance(operator, IsCommutative) and
              rhs == operator.identity_element):
            return lhs

    if isinstance(operator, HasZeroElement) and operator.has_zero_element:
        if (isinstance(operator, IsAdditionLike) and operator.is_addition_like and
                (lhs == operator.zero_element or rhs == operator.zero_element)):
            return lhs if rhs == operator.zero_element else rhs
        elif (not isinstance(operator, IsAdditionLike) and
              (lhs == operator.zero_element or rhs == operator.zero_element)):
            return operator.zero_element

    # Use the operator's Python function
    if isinstance(operator, HasOperatorFunction):
        return operator.op_func(lhs, rhs)
    else:
        raise ValueError(
            f"Operator {type(operator)} does not have an operator function")


def _apply_binary_symbolic(operator: BinaryOperator, lhs: Any, rhs: Any) -> BinaryOperator:
    """Apply a binary operator to symbolic operands."""
    # Apply identity and zero simplifications first
    if isinstance(operator, HasIdentity) and operator.has_identity:
        if (isinstance(operator, IsCommutative) and operator.is_commutative and
                (lhs == operator.identity_element or rhs == operator.identity_element)):
            return lhs if rhs == operator.identity_element else rhs
        elif (not isinstance(operator, IsCommutative) and
              rhs == operator.identity_element):
            return lhs

    if isinstance(operator, HasZeroElement) and operator.has_zero_element:
        if (isinstance(operator, IsAdditionLike) and operator.is_addition_like and
                (lhs == operator.zero_element or rhs == operator.zero_element)):
            return lhs if rhs == operator.zero_element else rhs
        elif (not isinstance(operator, IsAdditionLike) and
              (lhs == operator.zero_element or rhs == operator.zero_element)):
            return operator.zero_element

    # Create symbolic operator using the operator's create_instance method
    return operator.create_instance(lhs, rhs)


def _apply_commutative_simplifications(node: BinaryOperator) -> Any:
    """Apply commutative simplifications (reordering)."""
    if not isinstance(node, IsCommutative) or not node.is_commutative:
        return node

    # Put constants on the right for all commutative operators
    if (isinstance(node.lhs, (int, float)) and
            not isinstance(node.rhs, (int, float))):
        return node.create_instance(node.rhs, node.lhs)

    return node


def _apply_constant_folding(node: BinaryOperator) -> Any:
    """Apply constant folding (evaluate numeric expressions)."""
    # Constant folding: (2+3) -> 5, (6*2) -> 12, etc.
    if (isinstance(node.lhs, (int, float)) and
            isinstance(node.rhs, (int, float))):
        if isinstance(node, HasOperatorFunction):
            return node.op_func(node.lhs, node.rhs)
        else:
            raise ValueError(
                f"Operator {type(node)} does not have an operator function")

    return node


def _apply_identity_simplifications(node: BinaryOperator) -> Any:
    """Apply identity element simplifications."""
    if not isinstance(node, HasIdentity) or not node.has_identity:
        return node

    identity = node.identity_element

    # x op identity -> x (for commutative operators)
    if (isinstance(node, IsCommutative) and node.is_commutative and
            (node.lhs == identity or node.rhs == identity)):
        return node.lhs if node.rhs == identity else node.rhs

    # For non-commutative operators, only simplify on the appropriate side
    if not isinstance(node, IsCommutative) and node.rhs == identity:
        return node.lhs

    return node


def _apply_unary_numeric(operator: UnaryOperator,
                        operand: Union[int, float]) -> Union[int, float]:
    """Apply a unary operator to a numeric operand using Python's operator module."""
    # Apply identity and zero simplifications first
    if isinstance(operator, HasIdentity) and operator.has_identity:
        if operand == operator.identity_element:
            return operand

    # Use the operator's Python function
    if isinstance(operator, HasOperatorFunction):
        return operator.op_func(operand)
    else:
        raise ValueError(
            f"Operator {type(operator)} does not have an operator function")


def _apply_unary_symbolic(operator: UnaryOperator, operand: Any) -> UnaryOperator:
    """Apply a unary operator to a symbolic operand."""
    # Apply identity simplifications
    if isinstance(operator, HasIdentity) and operator.has_identity:
        if operand == operator.identity_element:
            return operand

    # Create symbolic operator using the operator's create_instance method
    return operator.create_instance(operand)


def _apply_zero_simplifications(node: BinaryOperator) -> Any:
    """Apply zero element simplifications."""
    if not isinstance(node, HasZeroElement) or not node.has_zero_element:
        return node

    zero = node.zero_element

    # x op 0 -> x (for addition-like operators)
    if (isinstance(node, IsAdditionLike) and node.is_addition_like and
            (node.lhs == zero or node.rhs == zero)):
        return node.lhs if node.rhs == zero else node.rhs

    # 0 op x -> 0 (for multiplication-like operators)
    if (not isinstance(node, IsAdditionLike) and
            (node.lhs == zero or node.rhs == zero)):
        return zero

    return node


def _flatten_associative_commutative(node, op_type):
    """Flatten a tree of associative/commutative operators into a list of leaves."""
    items = []

    def _recurse(n):
        if isinstance(n, op_type):
            _recurse(n.lhs)
            _recurse(n.rhs)
        else:
            items.append(n)

    _recurse(node)
    return items


def _simplify_binary(node: BinaryOperator) -> Any:
    """Simplify a binary operator expression."""
    # Simplify both operands first
    lhs_simplified = simplify(node.lhs)
    rhs_simplified = simplify(node.rhs)

    # Apply the operator
    result = apply_binary_operator(node, lhs_simplified, rhs_simplified)

    # If associative and commutative, flatten and combine constants
    if (isinstance(result, IsAssociative) and result.is_associative and
            isinstance(result, IsCommutative) and result.is_commutative):
        leaves = _flatten_associative_commutative(result, type(result))
        const = 0
        nonconst = []
        for leaf in leaves:
            if isinstance(leaf, (int, float)):
                const += leaf
            else:
                nonconst.append(leaf)
        # Build the tree: all non-constants, then the constant if nonzero
        if const != 0:
            nonconst.append(const)
        if not nonconst:
            return 0 if hasattr(result, 'zero_element') else const
        expr = nonconst[0]
        for n in nonconst[1:]:
            expr = type(result)(expr, n)
        return expr

    # Apply binary-specific simplifications based on algebraic properties
    while isinstance(result, BinaryOperator):
        old_result = result
        result = _apply_identity_simplifications(result)
        result = _apply_zero_simplifications(result)
        result = _apply_constant_folding(result)
        result = _apply_associative_simplifications(result)
        result = _apply_commutative_simplifications(result)
        if result == old_result:
            break
    return result


def _simplify_expr(node: Any) -> Any:
    """
    Simplify a scalar or symbolic expression node using algebraic properties.
    """
    if isinstance(node, MatrixElement):
        return node
    if isinstance(node, (int, float)):
        return node
    if isinstance(node, UnaryOperator):
        return _simplify_unary(node)
    if isinstance(node, BinaryOperator):
        return _simplify_binary(node)
    raise TypeError(f"Unsupported type in expression tree: {type(node)}")


def _simplify_unary(node: UnaryOperator) -> Any:
    """Simplify a unary operator expression."""
    # Simplify the operand first
    lhs_simplified = simplify(node.lhs)

    # Apply the operator
    result = apply_unary_operator(node, lhs_simplified)

    # Apply unary-specific simplifications
    if isinstance(result, type(node)):
        # Double negation: -(-x) -> x (for any unary operator that is its own inverse)
        if isinstance(result.lhs, type(node)):
            return result.lhs.lhs

    return result


def apply_binary_operator(operator: BinaryOperator, lhs: Any, rhs: Any) -> Any:
    """
    Apply a binary operator to two operands.
    This function handles numeric and symbolic operands.
    """
    if is_numeric(lhs) and is_numeric(rhs):
        return _apply_binary_numeric(operator, lhs, rhs)
    else:
        return _apply_binary_symbolic(operator, lhs, rhs)


def apply_operator(operator: Operator, *operands) -> Any:
    """
    Apply an operator to its operands.
    This function is primarily for unary operators.
    """
    if len(operands) == 1:
        return apply_unary_operator(operator, operands[0])
    elif len(operands) == 2:
        return apply_binary_operator(operator, operands[0], operands[1])
    else:
        raise ValueError(
            f"Operator {type(operator)} expects 1 or 2 operands, got {len(operands)}.")


def apply_unary_operator(operator: UnaryOperator, operand: Any) -> Any:
    """
    Apply a unary operator to an operand.
    This function handles numeric and symbolic operands.
    """
    if is_numeric(operand):
        return _apply_unary_numeric(operator, operand)
    else:
        return _apply_unary_symbolic(operator, operand)


def is_numeric(v: Any) -> bool:
    """Check if a value is a numeric type (int or float)."""
    return isinstance(v, (int, float))


def simplify(node: Any) -> Any:
    """
    Universal simplify function: simplifies scalars, symbolic expressions, or matrices.
    If given a matrix (list of lists), recursively simplifies every element.
    """
    # Matrix: list of lists
    if isinstance(node, list) and node and all(isinstance(row, list) for row in node):
        return [[simplify(elem) for elem in row] for row in node]
    # Scalar or symbolic expression
    return _simplify_expr(node)


# =============================================================================
# Matrix Functions (lexicographically ordered)
# =============================================================================


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


def mat_cofactor_signs(m: List[List]) -> List[List]:
    """Apply cofactor signs to a matrix (multiply by (-1)^(i+j))."""
    return mat_visit_index(m, lambda v, i, j: v if (i + j) % 2 == 0 else Negate(v))


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


def mat_is_equal(lhs: List[List], rhs: List[List], tolerance: float = 1e-10) -> bool:
    """
    Check if two matrices are approximately equal.

    Args:
        lhs: First matrix
        rhs: Second matrix
        tolerance: Maximum allowed difference between elements

    Returns:
        True if matrices are approximately equal, False otherwise
    """
    if len(lhs) != len(rhs):
        return False
    for i in range(len(lhs)):
        if len(lhs[i]) != len(rhs[i]):
            return False
        for j in range(len(lhs[i])):
            if not math.isclose(lhs[i][j], rhs[i][j], rel_tol=tolerance, abs_tol=tolerance):
                return False
    return True


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
        raise ValueError(
            f"Matrix dimensions incompatible: {len(m)}x{len(m[0])} and {len(n)}x{len(n[0])}")

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


def mat_print(m: List[List]) -> None:
    """Print a matrix to the console."""
    for row in m:
        print(" ".join(str(elem) for elem in row))


def mat_smart_print(m: List[List]) -> None:
    """Print a matrix to the console using smart formatting for expressions."""
    for row in m:
        print(" ".join(_smart_str(elem) for elem in row))


def mat_python(m: List[List]) -> None:
    """Print a matrix in Python list format."""
    print(m)


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


def mat_transpose(m: List[List]) -> List[List]:
    """Transpose a matrix."""
    if not m:
        return []
    rows, cols = len(m), len(m[0])
    result = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = m[i][j]
    return result


def mat_symbolic(size: int) -> List[List]:
    """Create a symbolic matrix of given size with MatrixElement objects."""
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(MatrixElement(i, j))
        matrix.append(row)
    return matrix


def roughly_equal(a: float, b: float, tolerance: float = 1e-10) -> bool:
    """Check if two floats are approximately equal."""
    return abs(a - b) < tolerance


def _get_precedence(operator_type) -> int:
    """Get the precedence level of an operator (higher = tighter binding)."""
    if operator_type == Negate:
        return 4  # Highest precedence
    elif operator_type in (Multiply, Divide):
        return 3
    elif operator_type in (Add, Subtract):
        return 2
    else:
        return 1  # Default low precedence


def _needs_parentheses(node, parent_operator_type=None) -> bool:
    """Determine if a node needs parentheses when printed under a parent operator."""
    if not isinstance(node, (UnaryOperator, BinaryOperator)):
        return False
    
    if parent_operator_type is None:
        return False
    
    node_precedence = _get_precedence(type(node))
    parent_precedence = _get_precedence(parent_operator_type)
    
    # Need parentheses if node has lower precedence than parent
    if node_precedence < parent_precedence:
        return True
    
    # For same precedence, need parentheses for non-commutative operations
    if node_precedence == parent_precedence:
        if parent_operator_type in (Subtract, Divide):
            # For subtraction and division, right operand needs parentheses
            # if it's a binary operator of same precedence
            if isinstance(node, BinaryOperator):
                return True
    
    return False


def _smart_str(node, parent_operator_type=None) -> str:
    """Convert a node to string with minimal parentheses based on precedence."""
    if isinstance(node, MatrixElement):
        return str(node)
    elif isinstance(node, (int, float)):
        return str(node)
    elif isinstance(node, UnaryOperator):
        operand_str = _smart_str(node.lhs, type(node))
        # Unary operators don't need parentheses around their operand
        return f"{node.symbol()}{operand_str}"
    elif isinstance(node, BinaryOperator):
        lhs_str = _smart_str(node.lhs, type(node))
        rhs_str = _smart_str(node.rhs, type(node))
        result = f"{lhs_str}{node.symbol()}{rhs_str}"
        
        # Add parentheses if needed
        if _needs_parentheses(node, parent_operator_type):
            result = f"({result})"
        
        return result
    else:
        return str(node)


def smart_print(node: Any) -> None:
    """Print a node with minimal parentheses based on operator precedence."""
    print(_smart_str(node))


# =============================================================================
# Test Functions and Utilities (lexicographically ordered)
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
    """Decorator to mark a test function for parameterized execution."""

    def decorator(fn: Callable) -> Callable:
        # Mark as decorated and store the range
        fn._decorated = True
        fn._n_range = n_range
        return fn

    return decorator


def test(fn: Callable) -> None:
    """Run a test function and print results."""
    print(f"Running Test: {fn.__name__}")
    print(f"  Result: {fn()}")


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


@decorate_test
def test_mat_determinant_multiplication():
    """Test that det(A × B) = det(A) × det(B) for square matrices."""
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    AB = mat_multiply(A, B)
    det_AB = mat_determinant(AB)
    simplified_det_AB = simplify(det_AB)
    det_A = mat_determinant(A)
    det_B = mat_determinant(B)
    det_A_times_det_B = Multiply(det_A, det_B)
    simplified_det_A_times_det_B = simplify(det_A_times_det_B)
    print(f"A: {A}\nB: {B}\nAB: {AB}")
    print(f"det(AB): {det_AB} -> simplified: {simplified_det_AB}")
    print(f"det(A): {det_A}, det(B): {det_B}, det(A)*det(B): {det_A_times_det_B} -> simplified: {simplified_det_A_times_det_B}")
    diff = abs(simplified_det_AB - simplified_det_A_times_det_B)
    print(f"Difference: {diff}")
    assert diff < 1e-10
    return True


@decorate_test_n(range(2, 6))
def test_mat_determinant_n(i: int):
    """Test determinant of nxn identity matrices."""
    return mat_determinant(mat_identity(i))


@decorate_test_n(range(2, 6))
def test_mat_determinant_of_identity_is_one(i: int):
    """Test that determinant of identity matrix is 1."""
    return assert_result(simplify(mat_determinant(mat_identity(i))) == 1)


@decorate_test
def test_mat_determinant_properties():
    """Test additional determinant properties."""
    # Create test matrices
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    # Test det(kA) = k^n * det(A) where n is the size of the matrix
    k = 3
    kA = mat_scalar_multiply(A, k)
    det_kA = mat_determinant(kA)
    simplified_det_kA = simplify(det_kA)

    det_A = mat_determinant(A)
    simplified_det_A = simplify(det_A)
    expected_det_kA = simplified_det_A * (k ** 2)  # 2x2 matrix, so k^2

    assert abs(simplified_det_kA - expected_det_kA) < 1e-10

    # Test det(Aᵀ) = det(A)
    A_transpose = mat_transpose(A)
    det_A_transpose = mat_determinant(A_transpose)
    simplified_det_A_transpose = simplify(det_A_transpose)

    assert abs(simplified_det_A - simplified_det_A_transpose) < 1e-10

    return True


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
    identity = mat_identity(i)
    inv = mat_inverse(identity)
    simplified_inv = simplify(inv)
    print(f"Identity({i}): {identity}\nInverse: {inv}\nSimplified Inverse: {simplified_inv}")
    result = mat_is_equal(identity, simplified_inv)
    print(f"mat_is_equal(identity, simplified_inv): {result}")
    return assert_result(result)


@decorate_test
def test_mat_inverse_properties():
    """Test inverse properties: (A × B)⁻¹ = B⁻¹ × A⁻¹ and (A⁻¹)⁻¹ = A."""
    A = [[4, 7], [2, 6]]
    B = [[3, 1], [1, 2]]
    AB = mat_multiply(A, B)
    AB_inverse = mat_inverse(AB)
    simplified_AB_inverse = simplify(AB_inverse)
    A_inverse = mat_inverse(A)
    B_inverse = mat_inverse(B)
    B_inverse_A_inverse = mat_multiply(B_inverse, A_inverse)
    simplified_B_inverse_A_inverse = simplify(B_inverse_A_inverse)
    print(f"A: {A}\nB: {B}\nAB: {AB}\nAB_inverse: {AB_inverse}\nSimplified AB_inverse: {simplified_AB_inverse}\nB_inverse: {B_inverse}\nA_inverse: {A_inverse}\nB_inverse_A_inverse: {B_inverse_A_inverse}\nSimplified B_inverse_A_inverse: {simplified_B_inverse_A_inverse}")
    result1 = mat_is_equal(simplified_AB_inverse, simplified_B_inverse_A_inverse, tolerance=1e-10)
    print(f"mat_is_equal(simplified_AB_inverse, simplified_B_inverse_A_inverse): {result1}")
    A_inverse_inverse = mat_inverse(A_inverse)
    simplified_A_inverse_inverse = simplify(A_inverse_inverse)
    result2 = mat_is_equal(simplified_A_inverse_inverse, A, tolerance=1e-10)
    print(f"A_inverse_inverse: {A_inverse_inverse}\nSimplified: {simplified_A_inverse_inverse}\nmat_is_equal(simplified_A_inverse_inverse, A): {result2}")
    assert result1 and result2
    return True


@decorate_test
def test_mat_inverse_scale():
    """Test inverse of a scaled identity matrix."""
    mat = mat_identity(4)
    mat[1][1] = 10
    inv = mat_inverse(mat)
    inv = simplify(inv)

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
    inv = simplify(mat_inverse(mat))
    result = mat_multiply(mat, inv)
    result = simplify(result)

    assert roughly_equal(result[0][0], 1.0)
    assert roughly_equal(result[1][1], 1.0)
    assert roughly_equal(result[2][2], 1.0)
    assert roughly_equal(result[3][3], 1.0)
    return True


@decorate_test
def test_mat_minor():
    """Test minor matrix computation."""
    return mat_minor(mat_identity(3), 0, 1)


@decorate_test
def test_mat_multiply():
    """Test matrix multiplication."""
    return mat_multiply(mat_identity(3), mat_symbolic(3))


@decorate_test
def test_mat_multiply_associativity():
    """Test that matrix multiplication is associative: (A × B) × C = A × (B × C)."""
    # Create test matrices
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = [[9, 10], [11, 12]]

    # Compute (A × B) × C
    AB = mat_multiply(A, B)
    left_result = mat_multiply(AB, C)
    simplified_left = simplify(left_result)

    # Compute A × (B × C)
    BC = mat_multiply(B, C)
    right_result = mat_multiply(A, BC)
    simplified_right = simplify(right_result)

    # Verify associativity
    assert mat_is_equal(simplified_left, simplified_right, tolerance=1e-10)
    return True


@decorate_test
def test_mat_multiply_distributivity():
    """Test matrix multiplication distributivity: A × (B + C) = A × B + A × C."""
    # Create test matrices
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = [[9, 10], [11, 12]]

    # Compute A × (B + C)
    B_plus_C = mat_visit_index(B, lambda val, i, j: Add(val, C[i][j]))
    left_result = mat_multiply(A, B_plus_C)
    simplified_left = simplify(left_result)

    # Compute A × B + A × C
    A_times_B = mat_multiply(A, B)
    A_times_C = mat_multiply(A, C)
    right_result = mat_visit_index(A_times_B, lambda val, i, j: Add(val, A_times_C[i][j]))
    simplified_right = simplify(right_result)

    # Verify distributivity
    assert mat_is_equal(simplified_left, simplified_right, tolerance=1e-10)
    return True


@decorate_test
def test_mat_multiply_identity_left():
    """Test left identity property: I × A = A for any matrix A."""
    # Test with different sized matrices
    test_matrices = [
        [[1, 2], [3, 4]],  # 2x2
        [[1, 2, 3], [4, 5, 6]],  # 2x3
        [[1], [2], [3]],  # 3x1
    ]

    for matrix in test_matrices:
        rows = len(matrix)
        identity = mat_identity(rows)
        product = mat_multiply(identity, matrix)
        simplified_product = simplify(product)

        assert mat_is_equal(simplified_product, matrix, tolerance=1e-10)

    return True


@decorate_test
def test_mat_multiply_identity_right():
    """Test right identity property: A × I = A for any matrix A."""
    # Test with different sized matrices
    test_matrices = [
        [[1, 2], [3, 4]],  # 2x2
        [[1, 2, 3], [4, 5, 6]],  # 2x3
        [[1], [2], [3]],  # 3x1
    ]

    for matrix in test_matrices:
        cols = len(matrix[0])
        identity = mat_identity(cols)
        product = mat_multiply(matrix, identity)
        simplified_product = simplify(product)

        assert mat_is_equal(simplified_product, matrix, tolerance=1e-10)

    return True


@decorate_test
def test_mat_multiply_non_commutativity():
    """Test that matrix multiplication is not commutative: A × B ≠ B × A in general."""
    # Create test matrices
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    # Compute A × B
    AB = mat_multiply(A, B)
    simplified_AB = simplify(AB)

    # Compute B × A
    BA = mat_multiply(B, A)
    simplified_BA = simplify(BA)

    # Verify they are NOT equal (non-commutativity)
    assert not mat_is_equal(simplified_AB, simplified_BA, tolerance=1e-10)

    return True


@decorate_test
def test_mat_multiply_power_properties():
    """Test matrix power properties using repeated multiplication."""
    # Create test matrix
    A = [[1, 1], [0, 1]]

    # Compute A² = A × A
    A_squared = mat_multiply(A, A)
    simplified_A_squared = simplify(A_squared)

    # Compute A³ = A × A²
    A_cubed = mat_multiply(A, A_squared)
    simplified_A_cubed = simplify(A_cubed)

    # Verify A³ = A × A × A
    A_times_A_times_A = mat_multiply(A, mat_multiply(A, A))
    simplified_A_times_A_times_A = simplify(A_times_A_times_A)
    assert mat_is_equal(simplified_A_cubed, simplified_A_times_A_times_A, tolerance=1e-10)

    return True


@decorate_test
def test_mat_multiply_with_zero():
    """Test matrix multiplication with zero matrix."""
    # Create test matrices
    A = [[1, 2], [3, 4]]
    zero_matrix = [[0, 0], [0, 0]]

    # Test A × 0 = 0
    A_times_zero = mat_multiply(A, zero_matrix)
    simplified_A_times_zero = simplify(A_times_zero)
    assert mat_is_equal(simplified_A_times_zero, zero_matrix, tolerance=1e-10)

    # Test 0 × A = 0
    zero_times_A = mat_multiply(zero_matrix, A)
    simplified_zero_times_A = simplify(zero_times_A)
    assert mat_is_equal(simplified_zero_times_A, zero_matrix, tolerance=1e-10)

    return True


@decorate_test
def test_mat_operations_edge_cases():
    """Test matrix operations with edge cases."""
    # Test 1x1 matrices
    A_1x1 = [[5]]
    B_1x1 = [[3]]

    # Test multiplication
    AB_1x1 = mat_multiply(A_1x1, B_1x1)
    simplified_AB_1x1 = simplify(AB_1x1)
    assert simplified_AB_1x1 == [[15]]

    # Test determinant
    det_A_1x1 = mat_determinant(A_1x1)
    simplified_det_A_1x1 = simplify(det_A_1x1)
    assert simplified_det_A_1x1 == 5

    # Test transpose
    A_1x1_transpose = mat_transpose(A_1x1)
    assert A_1x1_transpose == [[5]]

    # Test scalar operations
    kA_1x1 = mat_scalar_multiply(A_1x1, 2)
    simplified_kA_1x1 = simplify(kA_1x1)
    assert simplified_kA_1x1 == [[10]]

    # Test identity matrix for 1x1
    I_1x1 = mat_identity(1)
    assert I_1x1 == [[1]]

    # Test I × A = A for 1x1
    I_times_A_1x1 = mat_multiply(I_1x1, A_1x1)
    simplified_I_times_A_1x1 = simplify(I_times_A_1x1)
    assert simplified_I_times_A_1x1 == [[5]]

    return True


@decorate_test
def test_mat_operations_with_identity():
    """Test various matrix operations with identity matrices."""
    # Test different sized identity matrices
    for size in [2, 3, 4]:
        I = mat_identity(size)

        # Test I × I = I
        I_times_I = mat_multiply(I, I)
        simplified_I_times_I = simplify(I_times_I)
        assert mat_is_equal(simplified_I_times_I, I, tolerance=1e-10)

        # Test det(I) = 1
        det_I = mat_determinant(I)
        simplified_det_I = simplify(det_I)
        assert abs(simplified_det_I - 1) < 1e-10

        # Test I⁻¹ = I
        I_inverse = mat_inverse(I)
        simplified_I_inverse = simplify(I_inverse)
        assert mat_is_equal(simplified_I_inverse, I, tolerance=1e-10)

        # Test Iᵀ = I
        I_transpose = mat_transpose(I)
        assert mat_is_equal(I_transpose, I, tolerance=1e-10)

    return True


@decorate_test_n(range(2, 6))
def test_mat_rank_n(i: int):
    """Test matrix rank computation."""
    return assert_result(mat_rank(mat_symbolic(i)) == i)


@decorate_test
def test_mat_scalar_divide():
    """Test scalar division of matrix."""
    return mat_scalar_divide(mat_symbolic(4), 64)


@decorate_test
def test_mat_scalar_multiply():
    """Test scalar multiplication of matrix."""
    return mat_scalar_multiply(mat_symbolic(4), 64)


@decorate_test
def test_mat_scalar_multiply_properties():
    """Test scalar multiplication properties: k(A × B) = (kA) × B = A × (kB)."""
    # Create test matrices
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    k = 3

    # Compute k(A × B)
    AB = mat_multiply(A, B)
    k_AB = mat_scalar_multiply(AB, k)
    simplified_k_AB = simplify(k_AB)

    # Compute (kA) × B
    kA = mat_scalar_multiply(A, k)
    kA_B = mat_multiply(kA, B)
    simplified_kA_B = simplify(kA_B)

    # Compute A × (kB)
    kB = mat_scalar_multiply(B, k)
    A_kB = mat_multiply(A, kB)
    simplified_A_kB = simplify(A_kB)

    # Verify all are equal
    assert mat_is_equal(simplified_k_AB, simplified_kA_B, tolerance=1e-10)
    assert mat_is_equal(simplified_k_AB, simplified_A_kB, tolerance=1e-10)

    return True


@decorate_test
def test_simplification_limitations():
    """Test to demonstrate current simplification capabilities."""
    # Create a symbolic element
    A = MatrixElement(0, 0, "m")

    # Test nested multiplication: ((A*2)*2) should simplify to (A*4)
    expr1 = Multiply(Multiply(A, 2), 2)
    simplified1 = simplify(expr1)
    print(f"((A*2)*2) = {expr1}")
    print(f"Simplified: {simplified1}")
    print(f"Expected: A*4, Got: {simplified1}")
    success1 = str(simplified1) == "(m[0][0]*4)"

    # Test addition of constants: (A*(2+3)) should simplify to (A*5)
    expr2 = Multiply(A, Add(2, 3))
    simplified2 = simplify(expr2)
    print(f"(A*(2+3)) = {expr2}")
    print(f"Simplified: {simplified2}")
    print(f"Expected: A*5, Got: {simplified2}")
    success2 = str(simplified2) == "(m[0][0]*5)"

    # Test zero elimination: (A*0) should simplify to 0
    expr3 = Multiply(A, 0)
    simplified3 = simplify(expr3)
    print(f"(A*0) = {expr3}")
    print(f"Simplified: {simplified3}")
    print(f"Expected: 0, Got: {simplified3}")
    success3 = simplified3 == 0

    print(f"Results: nested_mult={success1}, const_add={success2}, zero_elim={success3}")
    return success1 and success2 and success3


@decorate_test
def test_apply_functions():
    """Test that the centralized apply functions work correctly."""
    A = MatrixElement(0, 0, "m")

    # Test unary operators
    negate_op = Negate(A)
    result1 = apply_unary_operator(negate_op, 5)
    result2 = apply_unary_operator(negate_op, A)
    print(f"apply_unary_operator(Negate, 5) = {result1}")
    print(f"apply_unary_operator(Negate, A) = {result2}")

    # Test binary operators
    add_op = Add(A, A)
    result3 = apply_binary_operator(add_op, 3, 4)
    result4 = apply_binary_operator(add_op, A, A)
    print(f"apply_binary_operator(Add, 3, 4) = {result3}")
    print(f"apply_binary_operator(Add, A, A) = {result4}")

    # Test multiplication
    mult_op = Multiply(A, A)
    result5 = apply_binary_operator(mult_op, 2, 3)
    result6 = apply_binary_operator(mult_op, A, A)
    print(f"apply_binary_operator(Multiply, 2, 3) = {result5}")
    print(f"apply_binary_operator(Multiply, A, A) = {result6}")

    # Test identity and zero simplifications
    add_zero = apply_binary_operator(add_op, 5, 0)
    mult_one = apply_binary_operator(mult_op, 7, 1)
    mult_zero = apply_binary_operator(mult_op, 5, 0)
    print(f"5 + 0 = {add_zero}")
    print(f"7 * 1 = {mult_one}")
    print(f"5 * 0 = {mult_zero}")

    results = {
        'negate_numeric': result1 == -5,
        'negate_symbolic': isinstance(result2, Negate),
        'add_numeric': result3 == 7,
        'add_symbolic': isinstance(result4, Add),
        'mult_numeric': result5 == 6,
        'mult_symbolic': isinstance(result6, Multiply),
        'add_zero': add_zero == 5,
        'mult_one': mult_one == 7,
        'mult_zero': mult_zero == 0
    }
    print(f"Results: {results}")
    return all(results.values())


@decorate_test
def test_nested_simplification():
    """Test that nested expressions are fully simplified."""
    # Create the expression: Add(2, Add(MatrixElement(2,2), Add(4,5)))
    A = MatrixElement(2, 2)
    inner_add = Add(4, 5)  # This should simplify to 9
    middle_add = Add(A, inner_add)  # This should be A + 9
    outer_add = Add(2, middle_add)  # This should be 2 + (A + 9)

    print(f"Original expression: {outer_add}")
    print(f"Expected simplified: (m[2][2] + 11)")

    # Simplify the expression
    simplified = simplify(outer_add)
    print(f"Actual result: {simplified}")

    # The result should be (m[2][2] + 11)
    expected = str(simplified) == "(m[2][2]+11)"

    # Test a few more nested cases
    test2 = Add(Add(1, 2), Add(3, 4))  # Should simplify to 10
    simplified2 = simplify(test2)
    test2_passed = simplified2 == 10

    test3 = Add(Add(MatrixElement(0, 0), 5), Add(3, 2))  # Should be (m[0][0] + 10)
    simplified3 = simplify(test3)
    test3_passed = str(simplified3) == "(m[0][0]+10)"

    print(f"Test 2: {test2} -> {simplified2} (expected: 10)")
    print(f"Test 3: {test3} -> {simplified3} (expected: (m[0][0]+10))")

    return expected and test2_passed and test3_passed


@decorate_test
def test_matrix_elementwise_simplify():
    """Test that simplify works elementwise on a symbolic matrix."""
    # Create a 2x2 symbolic matrix with unsimplified expressions
    m = [[Add(1, 2), Multiply(2, 3)], [Add(4, 5), Multiply(6, 7)]]
    simplified = simplify(m)
    # The expected result is [[3, 6], [9, 42]]
    expected = [[3, 6], [9, 42]]
    print(f"Original: {m}")
    print(f"Simplified: {simplified}")
    return simplified == expected


@decorate_test
def test_smart_print():
    """Test smart printing with precedence rules to minimize parentheses."""
    # Test various expressions to show precedence handling
    A = MatrixElement(0, 0, "m")
    B = MatrixElement(1, 1, "m")
    
    # Test 1: Addition and multiplication precedence
    expr1 = Add(Multiply(A, 2), Multiply(B, 3))
    print(f"Expression 1: {expr1}")
    print(f"Smart print: ", end="")
    smart_print(expr1)
    # Should print: m[0][0]*2 + m[1][1]*3 (no parentheses needed)
    
    # Test 2: Subtraction with multiplication
    expr2 = Subtract(Multiply(A, 5), Multiply(B, 2))
    print(f"Expression 2: {expr2}")
    print(f"Smart print: ", end="")
    smart_print(expr2)
    # Should print: m[0][0]*5 - m[1][1]*2 (no parentheses needed)
    
    # Test 3: Division with addition
    expr3 = Divide(Add(A, B), 2)
    print(f"Expression 3: {expr3}")
    print(f"Smart print: ", end="")
    smart_print(expr3)
    # Should print: (m[0][0] + m[1][1])/2 (parentheses needed)
    
    # Test 4: Complex nested expression
    expr4 = Add(Multiply(A, Add(B, 1)), Subtract(5, Multiply(B, 2)))
    print(f"Expression 4: {expr4}")
    print(f"Smart print: ", end="")
    smart_print(expr4)
    # Should print: m[0][0]*(m[1][1] + 1) + 5 - m[1][1]*2
    
    # Test 5: Unary negation
    expr5 = Negate(Add(A, B))
    print(f"Expression 5: {expr5}")
    print(f"Smart print: ", end="")
    smart_print(expr5)
    # Should print: -(m[0][0] + m[1][1]) (parentheses needed)
    
    # Test 6: Matrix with smart printing
    matrix = [[Add(A, B), Multiply(A, 2)], [Subtract(B, A), Divide(A, B)]]
    print(f"Matrix with smart printing:")
    mat_smart_print(matrix)
    
    return True


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    print(f"{ANSI.HEADER}General Mathematics Library Test Suite{ANSI.ENDC}")
    print(f"{ANSI.BOLD}Running all tests...{ANSI.ENDC}\n")

    # Automatically detect and run all test functions with @decorate_test decorator
    import inspect
    import sys

    # Get all functions in the current module
    current_module = sys.modules[__name__]
    test_functions = []

    for name, obj in inspect.getmembers(current_module):
        # Check if it's a function and has the test decorator
        if (inspect.isfunction(obj) and
            name.startswith('test_') and
            hasattr(obj, '_decorated') and
            obj._decorated):
            test_functions.append((name, obj))

    # Sort all test functions (starting with 'test_') lexicographically by function name, including decorators and docstrings.
    test_functions.sort(key=lambda x: x[0])

    # Run all test functions
    for name, test_func in test_functions:
        print(f"{ANSI.OKBLUE}Running {name}...{ANSI.ENDC}")
        try:
            # Handle functions that take parameters (like range-based tests)
            if hasattr(test_func, '_n_range'):
                # For parameterized tests, run with all values in the range
                print("=" * 79)
                print(f"# Running Test: {name}")
                print("=" * 79)

                for i in test_func._n_range:
                    print()
                    try:
                        result = test_func(i)
                    except Exception:
                        result = None

                    print(f"  {name}({i}) = ", end="")
                    print(ANSI.OKGREEN, end="")
                    print(str(result))
                    print(ANSI.ENDC, end="")
                print()
            else:
                # For regular tests, just run them
                test_func()
        except Exception as e:
            print(f"{ANSI.FAIL}Error in {name}: {e}{ANSI.ENDC}")

    print(f"{ANSI.OKGREEN}{ANSI.BOLD}All tests completed!{ANSI.ENDC}")