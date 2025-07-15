class Operator:
	def symbol(self):
		raise NotImplementedError("symbol() not defined.")

class UnaryOperator(Operator):
	def __init__(self, lhs):
		self.lhs = lhs
	def apply(self, lhs):
		raise NotImplementedError("apply() not defjned.")
	def simplify(self):
		raise NotImplementedError("simplify() not defjned.")
	def __str__(self):
		return "(" + self.symbol() + str(self.lhs) + ")"
	def __repr__(self):
		return "(" + self.symbol() + str(self.lhs) + ")"

class BinaryOperator(Operator):
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs
	def apply(self, lhs, rhs):
		raise NotImplementedError("apply() not defjned.")
	def simplify(self):
		raise NotImplementedError("simplify() not defjned.")
	def __str__(self):
		return "(" + str(self.lhs) + self.symbol() + str(self.rhs) + ")"
	def __repr__(self):
		return "(" + str(self.lhs) + self.symbol() + str(self.rhs) + ")"

class Negate(UnaryOperator):
	def apply(self, lhs):
		return -lhs
	def symbol(self):
		return "-"
	def simplify(self):
		return -self.lhs.simplify()

class Add(BinaryOperator):
	def apply(self, lhs, rhs):
		return lhs + rhs
	def symbol(self):
		return "+"
	def simplify(self):
		return self.lhs.simplify() + self.rhs.simplify()

class Divide(BinaryOperator):
	def apply(self, lhs, rhs):
		return lhs / rhs
	def symbol(self):
		return "/"
	def simplify(self):
		return self.lhs.simplify() / self.rhs.simplify()

class Multiply(BinaryOperator):
	def apply(self, lhs, rhs):
		return lhs * rhs
	def symbol(self):
		return "*"
	def simplify(self):
		return self.lhs.simplify() * self.rhs.simplify()

class Subtract(BinaryOperator):
	def apply(self, lhs, rhs):
		return lhs - rhs
	def symbol(self):
		return "-"
	def simplify(self):
		return self.lhs.simplify() - self.rhs.simplify()

class MatrixElement:
	def __init__(self, i1, j1):
		self.i1 = i1
		self.j1 = j1
	def __str__(self):
		return "m[" + str(self.i1) + "][" + str(self.j1) + "]"
	def __repr__(self):
		return "m[" + str(self.i1) + "][" + str(self.j1) + "]"

def isNumeric(v):
	return True if (type(v) == int or type(v) == float) else False

def simplify(node):
	if (type(node) == MatrixElement):
		return node
	if (issubclass(type(node), UnaryOperator)):
		lhs = simplify(node.lhs)
		return node.apply(lhs)
	if (issubclass(type(node), BinaryOperator)):
		lhs = simplify(node.lhs)
		rhs = simplify(node.rhs)
		return node.apply(lhs, rhs)
	if (type(node) == int or type(node) == float):
		return node;
	raise TypeError("Bad type in expression tree.")

class Matrix:
	def __init__(self, m):
		self.m = m
	def Identity(i):
		i2 = []
		for i1 in range(i):
			j2 = []
			for j1 in range(i):
				j2.append(1 if i1 == j1 else 0)
			i2.append(j2)
		return Matrix(i2)
	def Print(self):
		for i1 in self.m:
			print(i1)

def matPrint(m):
	for i1 in m:
		print(i1)

def matCofactor(m):
	return matVisitIndex(m, lambda v, i, j : v if ((i + j) % 2 == 0) else Negate(v))

def matDeterminant(m):
	if (matRank(m) == -1):
		raise ValueError("Can't compute a determinant for a non-square matrix.")
	if (matRank(m) == 1):
		return m[0][0];
	if (matRank(m) == 2):
		a = Multiply(m[0][0], m[1][1])
		b = Multiply(m[0][1], m[1][0])
		return Subtract(a, b)
	runsum = None
	for j1 in range(len(m[0])):
		m2 = matMinor(m, 0, j1)
		m2 = matDeterminant(m2)
		m2 = Multiply(m[0][j1], m2)
		if (runsum == None):
			runsum = m2
		else:
			if (j1 % 2 == 0):
				runsum = Add(runsum, m2)
			else:
				runsum = Subtract(runsum, m2)
	return runsum

def matIsEqual(lhs, rhs):
	for i1 in range(len(lhs)):
		for j1 in range(len(lhs[i1])):
			if (lhs[i1][j1] != rhs[i1][j1]):
				return False
	return True

def matIdentity(size):
	i2 = []
	for i1 in range(size):
		j2 = []
		for j1 in range(size):
			j2.append(1 if i1 == j1 else 0)
		i2.append(j2)
	return i2

def matInverse(m):
	if (matRank(m) == -1):
		raise ValueError("Can't invert a non-square matrix.")
	i2 = []
	for i1 in range(len(m)):
		j2 = []
		for j1 in range(len(m[i1])):
			lhs = m[i1][j1]
			rhs = matMinor(m, i1, j1);
			rhs = matDeterminant(rhs)
			j2.append(Multiply(lhs, rhs));
		i2.append(j2)
	i2 = matCofactor(i2)
	i2 = matTranspose(i2)
	i2 = matScalarDivide(i2, matDeterminant(m))
	return i2

def matMinor(m, i, j):
	i2 = []
	for i1 in range(len(m)):
		if (i1 == i):
			continue
		j2 = []
		for j1 in range(len(m[i1])):
			if (j1 == j):
				continue
			j2.append(m[i1][j1])
		i2.append(j2)
	return i2

def matRank(m):
	size = len(m);
	for i1 in m:
		if (len(i1) != size):
			return -1
	return size

def matScalarDivide(lhs, rhs):
	return matVisit(lhs, lambda x : Divide(x, rhs))

def matScalarMultiply(lhs, rhs):
	return matVisit(lhs, lambda x : Multiply(x, rhs))

def matSimplify(m):
	return matVisit(m, lambda x : simplify(x))

def matSymbolic(size):
	i2 = []
	for i1 in range(size):
		j2 = []
		for j1 in range(size):
			j2.append(MatrixElement(i1, j1))
		i2.append(j2)
	return i2

def matTranspose(m):
	i2 = []
	for i1 in range(len(m)):
		j2 = []
		for j1 in range(len(m[i1])):
			j2.append(m[j1][i1])
		i2.append(j2)
	return i2

def matVisit(m, fn):
	i2 = []
	for i1 in m:
		j2 = []
		for j1 in i1:
			j2.append(fn(j1))
		i2.append(j2)
	return i2

def matVisitIndex(m, fn):
	i2 = []
	for i1 in range(len(m)):
		j2 = []
		for j1 in range(len(m[i1])):
			j2.append(fn(m[i1][j1], i1, j1))
		i2.append(j2)
	return i2

########################################
# Test Suite
########################################

class ANSI:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Assert(result):
	assert(result)
	return result

def test(fn):
	print("Running Test: " + fn.__name__)
	print("  Result: " + str(fn()))

def decorateTest(fn):
	print("###############################################################################")
	print("# Running Test: " + fn.__name__)
	print("###############################################################################")
	print()
	result = fn()
	print("  " + fn.__name__ + "() = ", end="")
	print(ANSI.OKGREEN, end="")
	print(str(result))
	print(ANSI.ENDC, end="")
	print()
	return fn

def decorateTestN(n):
	def decorator(fn):
		print("###############################################################################")
		print("# Running Test: " + fn.__name__)
		print("###############################################################################")
		for i in n:
			print()
			print("  " + fn.__name__ + "(" + str(i) + ") = ", end="")
			print(ANSI.OKGREEN, end="")
			print(str(fn(i)))
			print(ANSI.ENDC, end="")
	print()
	return decorator

@decorateTest
def testMatDeterminant2():
	return matDeterminant(matIdentity(2))

@decorateTest
def testMatDeterminant3():
	return matDeterminant(matIdentity(3))

@decorateTest
def testMatDeterminant4():
	return matDeterminant(matIdentity(4))

@decorateTestN(range(2, 6))
def testMatDeterminantN(i):
	return matDeterminant(matIdentity(i))

@decorateTestN(range(2, 6))
def testMatDeterminant_Of_Identity_Is_One(i):
	return Assert(simplify(matDeterminant(matIdentity(i))) == 1)

@decorateTest
def testMatIdentity2():
	return matIdentity(2)

@decorateTest
def testMatIdentity3():
	return matIdentity(3)

@decorateTest
def testMatIdentity4():
	return matIdentity(4)

@decorateTestN(range(2, 6))
def testMatIdentityN(i):
	return matIdentity(i)

# Inverse of an identity is still the identity.
@decorateTestN(range(2, 6))
def testMatInverseN(i):
	return Assert(matIsEqual(matIdentity(i), matSimplify(matInverse(matIdentity(i)))))

@decorateTest
def testMatMinor():
	return matMinor(matIdentity(3), 0, 1)

@decorateTest
def testMatScalarDivide():
	return matScalarDivide(matSymbolic(4), 64)

@decorateTest
def testMatScalarMultiply():
	return matScalarMultiply(matSymbolic(4), 64)

@decorateTestN(range(2, 6))
def testMatRankN(i):
	return Assert(matRank(matSymbolic(i)) == i)

@decorateTest
def testMatSimplify():
	return matSimplify(matScalarDivide(matScalarMultiply(matIdentity(4), 64), 64))

@decorateTestN(range(2, 6))
def testMatSymbolic(i):
	return matSymbolic(i)

@decorateTest
def testMatVisit():
	return matVisit(matSymbolic(4), lambda x : print(str(x)))
	
@decorateTest
def testMatVisitIndex():
	return matVisitIndex(matSymbolic(4), lambda x, i1, j1 : print(str(i1) + "," + str(j1) + "=" + str(x)))
