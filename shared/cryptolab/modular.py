"""
Modular arithmetic classes mirroring SageMath's Mod() and Zmod() API.

Mod(a, n) creates an element of Z/nZ with automatic wrapping.
Zmod(n) creates the ring Z/nZ with iteration, unit listing, and operation tables.
"""

from .number_theory import gcd, inverse_mod, power_mod, euler_phi


# ---------------------------------------------------------------------------
# Mod class: an element of Z/nZ
# ---------------------------------------------------------------------------

class Mod:
    """
    An element of Z/nZ with automatic modular arithmetic.

    Usage mirrors SageMath:
        a = Mod(3, 7)
        a + Mod(5, 7)   # -> 1
        a ** 2           # -> 2
        ~a               # -> 5  (modular inverse)
    """

    __slots__ = ('_value', '_modulus')

    def __init__(self, value, modulus):
        modulus = int(modulus)
        if modulus < 1:
            raise ValueError(f"Modulus must be positive, got {modulus}")
        self._modulus = modulus
        self._value = int(value) % modulus

    @property
    def value(self):
        return self._value

    @property
    def modulus(self):
        return self._modulus

    # --- Representation ---

    def __repr__(self):
        return str(self._value)

    def __str__(self):
        return str(self._value)

    def __int__(self):
        return self._value

    def __index__(self):
        return self._value

    def __float__(self):
        return float(self._value)

    # --- Comparison and hashing ---

    def _check_compatible(self, other):
        if isinstance(other, Mod):
            if self._modulus != other._modulus:
                raise ValueError(
                    f"Cannot combine Mod elements with different moduli "
                    f"({self._modulus} vs {other._modulus})"
                )
            return other._value
        return int(other)

    def __eq__(self, other):
        if isinstance(other, Mod):
            return self._value == other._value and self._modulus == other._modulus
        return self._value == int(other) % self._modulus

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # Must be consistent with __eq__: since Mod(4,12) == 4,
        # hash(Mod(4,12)) must equal hash(4).
        return hash(self._value)

    def __bool__(self):
        return self._value != 0

    # --- Arithmetic ---

    def __add__(self, other):
        v = self._check_compatible(other)
        return Mod(self._value + v, self._modulus)

    def __radd__(self, other):
        return Mod(int(other) + self._value, self._modulus)

    def __sub__(self, other):
        v = self._check_compatible(other)
        return Mod(self._value - v, self._modulus)

    def __rsub__(self, other):
        return Mod(int(other) - self._value, self._modulus)

    def __mul__(self, other):
        v = self._check_compatible(other)
        return Mod(self._value * v, self._modulus)

    def __rmul__(self, other):
        return Mod(int(other) * self._value, self._modulus)

    def __neg__(self):
        return Mod(-self._value, self._modulus)

    def __pow__(self, exp):
        exp = int(exp)
        if exp < 0:
            # Negative exponent: compute inverse first
            inv = inverse_mod(self._value, self._modulus)
            return Mod(power_mod(inv, -exp, self._modulus), self._modulus)
        return Mod(power_mod(self._value, exp, self._modulus), self._modulus)

    def __invert__(self):
        """~x returns the modular inverse."""
        return Mod(inverse_mod(self._value, self._modulus), self._modulus)

    def __truediv__(self, other):
        v = self._check_compatible(other)
        inv = inverse_mod(v, self._modulus)
        return Mod(self._value * inv, self._modulus)

    def __mod__(self, other):
        return Mod(self._value % int(other), self._modulus)

    # --- Ordering (useful for sorting) ---

    def __lt__(self, other):
        if isinstance(other, Mod):
            return self._value < other._value
        return self._value < int(other)

    def __le__(self, other):
        if isinstance(other, Mod):
            return self._value <= other._value
        return self._value <= int(other)

    # --- Group theory methods ---

    def multiplicative_order(self):
        """
        The smallest positive k such that self^k = 1 (mod n).
        Raises ValueError if self is not a unit.
        """
        if gcd(self._value, self._modulus) != 1:
            raise ValueError(
                f"{self._value} is not a unit mod {self._modulus} "
                f"(gcd = {gcd(self._value, self._modulus)})"
            )
        result = 1
        current = self._value
        while current != 1:
            current = (current * self._value) % self._modulus
            result += 1
        return result

    def additive_order(self):
        """
        The smallest positive k such that k * self = 0 (mod n).
        Equals n / gcd(self.value, n).
        """
        g = gcd(self._value, self._modulus)
        if g == 0:
            return 1
        return self._modulus // g

    def pow_verbose(self, exp):
        """Compute self^exp with step-by-step printing."""
        result = power_mod(self._value, int(exp), self._modulus, verbose=True)
        return Mod(result, self._modulus)

    def parent(self):
        """Return the ring this element belongs to (like SageMath's .parent())."""
        return ZmodRing(self._modulus)


# ---------------------------------------------------------------------------
# ZmodRing class: the ring Z/nZ
# ---------------------------------------------------------------------------

class ZmodRing:
    """
    The ring Z/nZ. Mirrors SageMath's Zmod(n) / Integers(n).

    Usage:
        R = Zmod(7)
        a = R(3)         # -> Mod(3, 7)
        list(R)          # -> [Mod(0,7), Mod(1,7), ..., Mod(6,7)]
        R.order()        # -> 7
        R.list_of_elements_of_multiplicative_group()  # units
    """

    def __init__(self, n):
        self._n = int(n)
        if self._n < 1:
            raise ValueError(f"Modulus must be positive, got {self._n}")

    def __repr__(self):
        return f"Ring of integers modulo {self._n}"

    def __call__(self, value):
        """Create a Mod element: R(3) -> Mod(3, n)."""
        return Mod(value, self._n)

    def __iter__(self):
        """Iterate over all elements: Mod(0,n), Mod(1,n), ..., Mod(n-1,n)."""
        for i in range(self._n):
            yield Mod(i, self._n)

    def __contains__(self, item):
        if isinstance(item, Mod):
            return item.modulus == self._n
        return True  # Any integer can be reduced mod n

    def order(self):
        """Number of elements in the ring."""
        return self._n

    def list(self):
        """All elements as a list."""
        return [Mod(i, self._n) for i in range(self._n)]

    def list_of_elements_of_multiplicative_group(self):
        """Units of Z/nZ: elements with gcd(a, n) = 1."""
        return [Mod(a, self._n) for a in range(1, self._n) if gcd(a, self._n) == 1]

    def addition_table(self, style='elements'):
        """
        Print the addition table for Z/nZ.
        style='elements' prints values, style='list' returns a 2D list.
        """
        n = self._n
        table = [[(i + j) % n for j in range(n)] for i in range(n)]
        if style == 'list':
            return table
        self._print_table(table, '+', list(range(n)))
        return None

    def multiplication_table(self, style='elements'):
        """
        Print the multiplication table for Z/nZ.
        style='elements' prints values, style='list' returns a 2D list.
        """
        n = self._n
        table = [[(i * j) % n for j in range(n)] for i in range(n)]
        if style == 'list':
            return table
        self._print_table(table, '*', list(range(n)))
        return None

    def _print_table(self, table, op, labels):
        """Format and print an operation table."""
        n = len(labels)
        # Determine column width
        w = max(len(str(x)) for row in table for x in row)
        w = max(w, len(str(max(labels))), len(op))

        # Header
        header = f"{op:>{w}} |" + "".join(f" {labels[j]:>{w}}" for j in range(n))
        print(header)
        print("-" * len(header))

        # Rows
        for i in range(n):
            row = f"{labels[i]:>{w}} |" + "".join(f" {table[i][j]:>{w}}" for j in range(n))
            print(row)


# ---------------------------------------------------------------------------
# Factory function
# ---------------------------------------------------------------------------

def Zmod(n):
    """Create the ring Z/nZ. Mirrors SageMath's Zmod(n)."""
    return ZmodRing(n)


def Integers(n):
    """Alias for Zmod(n). Mirrors SageMath's Integers(n)."""
    return ZmodRing(n)
