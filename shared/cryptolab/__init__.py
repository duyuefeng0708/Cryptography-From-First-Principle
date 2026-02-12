"""
cryptolab: pedagogical pure Python cryptography primitives.

Designed for teaching, not production. Readable over fast.
Pyodide-compatible (no C extensions).
"""

from .number_theory import (
    gcd,
    extended_gcd,
    euler_phi,
    factor,
    divisors,
    is_prime,
    power_mod,
    inverse_mod,
    primitive_root,
    crt,
    discrete_log,
)

from .modular import (
    Mod,
    Zmod,
    ZmodRing,
    Integers,
)

__all__ = [
    # number theory
    'gcd', 'extended_gcd', 'euler_phi', 'factor', 'divisors',
    'is_prime', 'power_mod', 'inverse_mod', 'primitive_root',
    'crt', 'discrete_log',
    # modular arithmetic
    'Mod', 'Zmod', 'ZmodRing', 'Integers',
]
