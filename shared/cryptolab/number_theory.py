"""
Pure Python number theory primitives for cryptography teaching.

Readable over fast. Every function is self-contained and easy to step through.
No C extensions, Pyodide-compatible.
"""

from math import isqrt


# ---------------------------------------------------------------------------
# Greatest common divisor
# ---------------------------------------------------------------------------

def gcd(a, b):
    """Euclidean algorithm. Returns the greatest common divisor of a and b."""
    a, b = abs(int(a)), abs(int(b))
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """
    Extended Euclidean algorithm.
    Returns (g, s, t) such that a*s + b*t = g = gcd(a, b).
    """
    a, b = int(a), int(b)
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


# ---------------------------------------------------------------------------
# Factorization and divisors
# ---------------------------------------------------------------------------

def factor(n):
    """
    Prime factorization by trial division.
    Returns a dict {prime: exponent}, e.g. factor(60) = {2: 2, 3: 1, 5: 1}.
    """
    n = abs(int(n))
    if n < 2:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def divisors(n):
    """All positive divisors of n, sorted."""
    n = abs(int(n))
    if n == 0:
        return []
    divs = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            divs.append(d)
            if d != n // d:
                divs.append(n // d)
    return sorted(divs)


def is_prime(n):
    """Primality test by trial division. Good enough for teaching-sized numbers."""
    n = int(n)
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0:
            return False
        d += 6
    return True


# ---------------------------------------------------------------------------
# Euler's totient
# ---------------------------------------------------------------------------

def euler_phi(n):
    """
    Euler's totient function via prime factorization.
    phi(n) = n * product of (1 - 1/p) for each prime p dividing n.
    """
    n = int(n)
    if n < 1:
        return 0
    result = n
    for p in factor(n):
        result = result // p * (p - 1)
    return result


# ---------------------------------------------------------------------------
# Modular exponentiation
# ---------------------------------------------------------------------------

def power_mod(base, exp, mod, verbose=False):
    """
    Square-and-multiply modular exponentiation.
    Computes base^exp mod mod.

    With verbose=True, prints each step of the algorithm.
    """
    base, exp, mod = int(base), int(exp), int(mod)
    if mod == 1:
        return 0

    # Handle negative exponents via modular inverse
    if exp < 0:
        base = inverse_mod(base, mod)
        exp = -exp

    if verbose:
        bits = bin(exp)[2:]
        print(f"Square-and-multiply for {base}^{exp} mod {mod}:")
        print(f"  {exp} = {bits} in binary ({len(bits)} bits)")

    result = 1
    base = base % mod
    bit_pos = 0

    temp_exp = exp
    while temp_exp > 0:
        bit = temp_exp & 1
        if bit:
            result = (result * base) % mod
            if verbose:
                print(f"  bit {bit_pos} = 1: multiply -> result = {result}")
        else:
            if verbose:
                print(f"  bit {bit_pos} = 0: skip")
        base = (base * base) % mod
        if verbose and temp_exp > 1:
            print(f"    square base -> {base}")
        temp_exp >>= 1
        bit_pos += 1

    if verbose:
        print(f"  Result: {result}")
    return result


# ---------------------------------------------------------------------------
# Modular inverse
# ---------------------------------------------------------------------------

def inverse_mod(a, n):
    """
    Modular inverse of a modulo n via the extended Euclidean algorithm.
    Raises ValueError if gcd(a, n) != 1.
    """
    a, n = int(a), int(n)
    g, s, _ = extended_gcd(a % n, n)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {n} (gcd = {g})")
    return s % n


# ---------------------------------------------------------------------------
# Primitive root
# ---------------------------------------------------------------------------

def primitive_root(p):
    """
    Find the smallest primitive root modulo p (p must be prime).
    A primitive root g has multiplicative order p-1.
    """
    p = int(p)
    if p == 2:
        return 1
    if not is_prime(p):
        raise ValueError(f"{p} is not prime")

    phi = p - 1
    prime_factors = list(factor(phi).keys())

    for g in range(2, p):
        if all(power_mod(g, phi // q, p) != 1 for q in prime_factors):
            return g
    raise ValueError(f"No primitive root found for {p}")  # Should not happen


# ---------------------------------------------------------------------------
# Chinese Remainder Theorem
# ---------------------------------------------------------------------------

def crt(remainders, moduli):
    """
    Chinese Remainder Theorem.
    Given remainders [r1, r2, ...] and moduli [m1, m2, ...],
    find x such that x = ri (mod mi) for all i.
    """
    remainders = [int(r) for r in remainders]
    moduli = [int(m) for m in moduli]

    if len(remainders) != len(moduli):
        raise ValueError("remainders and moduli must have the same length")

    # Iteratively combine pairs
    x, m = remainders[0], moduli[0]
    for i in range(1, len(remainders)):
        r2, m2 = remainders[i], moduli[i]
        g, s, _ = extended_gcd(m, m2)
        if (r2 - x) % g != 0:
            raise ValueError(f"No solution: {x} mod {m} and {r2} mod {m2} are incompatible")
        lcm = m // g * m2
        x = (x + m * s * ((r2 - x) // g)) % lcm
        m = lcm
    return x


# ---------------------------------------------------------------------------
# Discrete logarithm (baby-step giant-step)
# ---------------------------------------------------------------------------

def discrete_log(target, base, n):
    """
    Baby-step giant-step algorithm.
    Finds x such that base^x = target (mod n).
    Searches in range [0, n-1].
    """
    target, base, n = int(target) % n, int(base) % n, int(n)
    m = isqrt(n) + 1

    # Baby steps: base^j for j in [0, m)
    table = {}
    power = 1
    for j in range(m):
        table[power] = j
        power = (power * base) % n

    # Giant step factor: base^(-m) mod n
    inv = power_mod(base, n - 1 - ((m - 1) % (n - 1)), n) if n > 1 else 0
    # Simpler: inv = inverse of base^m mod n
    base_m = power_mod(base, m, n)
    if gcd(base_m, n) != 1:
        # Fallback to brute force for non-invertible case
        power = 1
        for x in range(n):
            if power == target:
                return x
            power = (power * base) % n
        raise ValueError(f"No discrete log found: {base}^x = {target} (mod {n})")

    inv_base_m = inverse_mod(base_m, n)

    # Giant steps: target * (base^(-m))^i
    gamma = target
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * inv_base_m) % n

    raise ValueError(f"No discrete log found: {base}^x = {target} (mod {n})")
