#!/usr/bin/env python3
"""Generate SageMath Jupyter notebook stubs for every module in the crypto teaching repo.

Usage:
    python3 scripts/gen_notebook_stubs.py

Generates .ipynb files under each module's sage/ directory.  Safe to re-run:
existing files are overwritten with identical content (idempotent).

No external dependencies beyond the Python 3 standard library.
"""

import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Repository root (one level up from scripts/)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Complete module / notebook specification  (69 notebooks, 12 modules)
#
# Structure:
#   key   = relative path from repo root to the module directory
#   value = list of (filename_stem, title, description, sections)
#       sections = list of (heading, sagemath_code_comment)
# ---------------------------------------------------------------------------
MODULES: dict[str, list[tuple[str, str, str, list[tuple[str, str]]]]] = {
    # ------------------------------------------------------------------
    # foundations/01  (6 notebooks)
    # ------------------------------------------------------------------
    "foundations/01-modular-arithmetic-groups": [
        (
            "01a-integers-and-division",
            "Integers and Division",
            "Review division algorithm, divmod, remainders",
            [
                ("The Division Algorithm",
                 "# Explore the division algorithm: a = q*b + r\n"
                 "a, b = 37, 7\n"
                 "q, r = divmod(a, b)\n"
                 "print(f'{a} = {q}*{b} + {r}')"),
                ("Remainders and Congruence",
                 "# Compute remainders for various values and observe patterns\n"
                 "for k in range(20):\n"
                 "    print(f'{k} mod 7 = {k % 7}')"),
                ("Computing with SageMath",
                 "# Use SageMath's Mod and divmod for exact arithmetic\n"
                 "print(divmod(100, 13))\n"
                 "print(Mod(100, 13))"),
            ],
        ),
        (
            "01b-modular-arithmetic",
            "Modular Arithmetic",
            "Congruences, Zmod(n), addition/multiplication tables",
            [
                ("Congruence Classes",
                 "# Create the ring Z/12Z and inspect its elements\n"
                 "R = Zmod(12)\n"
                 "print(list(R))"),
                ("Addition and Multiplication Tables",
                 "# Build and display the addition table for Z/7Z\n"
                 "R = Zmod(7)\n"
                 "R.addition_table('elements')"),
                ("Patterns in Multiplication",
                 "# Display the multiplication table and look for zero divisors\n"
                 "R = Zmod(12)\n"
                 "R.multiplication_table('elements')"),
            ],
        ),
        (
            "01c-groups-first-look",
            "Groups: A First Look",
            "Group axioms from Z_n examples, closure/identity/inverse",
            [
                ("Closure and the Binary Operation",
                 "# Verify closure: adding any two elements of Z_7 stays in Z_7\n"
                 "R = Zmod(7)\n"
                 "a, b = R(3), R(5)\n"
                 "print(a + b, a + b in R)"),
                ("Identity and Inverses",
                 "# Find the additive identity and inverses in Z_7\n"
                 "R = Zmod(7)\n"
                 "for x in R:\n"
                 "    print(f'inverse of {x} is {-x}')"),
                ("Checking the Group Axioms",
                 "# Verify associativity for a sample triple\n"
                 "R = Zmod(7)\n"
                 "a, b, c = R(2), R(4), R(6)\n"
                 "assert (a + b) + c == a + (b + c)"),
            ],
        ),
        (
            "01d-cyclic-groups-generators",
            "Cyclic Groups and Generators",
            "Generators, multiplicative_order(), powers",
            [
                ("Powers of an Element",
                 "# Compute successive powers of g in (Z/7Z)*\n"
                 "R = Zmod(7)\n"
                 "g = R(3)\n"
                 "print([g^k for k in range(7)])"),
                ("Generators and Orders",
                 "# Find the multiplicative order of each unit in Z/7Z\n"
                 "R = Zmod(7)\n"
                 "for x in R.list_of_elements_of_multiplicative_group():\n"
                 "    print(f'ord({x}) = {Mod(x,7).multiplicative_order()}')"),
                ("Identifying Generators",
                 "# A generator has order equal to the group size\n"
                 "R = Zmod(7)\n"
                 "phi = euler_phi(7)\n"
                 "gens = [x for x in range(1,7) if Mod(x,7).multiplicative_order() == phi]\n"
                 "print('Generators:', gens)"),
            ],
        ),
        (
            "01e-subgroups-lagrange",
            "Subgroups and Lagrange's Theorem",
            "Subgroup detection, Lagrange verification",
            [
                ("Finding Subgroups",
                 "# List all subgroups of Z/12Z (additive)\n"
                 "G = Zmod(12)\n"
                 "# Generate subgroup from element 4\n"
                 "elem = G(4)\n"
                 "subgroup = set()\n"
                 "x = elem\n"
                 "while x not in subgroup:\n"
                 "    subgroup.add(x)\n"
                 "    x = x + elem\n"
                 "print(sorted(subgroup))"),
                ("Lagrange's Theorem",
                 "# Verify that subgroup order divides group order\n"
                 "group_order = 12\n"
                 "for d in divisors(group_order):\n"
                 "    print(f'{d} divides {group_order}: {group_order % d == 0}')"),
                ("Cosets and Counting",
                 "# Compute cosets of a subgroup in Z/12Z\n"
                 "# TODO: build cosets and verify equal partition"),
            ],
        ),
        (
            "01f-group-visualization",
            "Visualizing Group Structure",
            "Cayley graphs, subgroup lattices",
            [
                ("Cayley Graphs",
                 "# Visualize Z/6Z with generator 1\n"
                 "G = Zmod(6)\n"
                 "# TODO: build and plot Cayley graph"),
                ("Subgroup Lattice Diagrams",
                 "# Draw the subgroup lattice of Z/12Z\n"
                 "# TODO: use SageMath poset for subgroup lattice"),
                ("Color-Coded Multiplication Tables",
                 "# Create a color-coded multiplication table\n"
                 "# TODO: matplotlib heatmap of Z/7Z multiplication"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # foundations/02  (6 notebooks)
    # ------------------------------------------------------------------
    "foundations/02-rings-fields-polynomials": [
        (
            "02a-what-is-a-ring",
            "What Is a Ring?",
            "Ring axioms, Z as ring, two operations",
            [
                ("Ring Axioms",
                 "# Verify ring axioms for Z: additive group + multiplicative monoid\n"
                 "# Distributive: a*(b+c) == a*b + a*c\n"
                 "a, b, c = 3, 5, 7\n"
                 "assert a*(b+c) == a*b + a*c"),
                ("Z as a Ring",
                 "# SageMath's ZZ is the ring of integers\n"
                 "R = ZZ\n"
                 "print(R)\n"
                 "print(R.is_commutative())"),
                ("Rings vs Groups",
                 "# A ring has TWO operations; a group has one\n"
                 "R = Zmod(12)\n"
                 "print('Zero:', R.zero())\n"
                 "print('One:', R.one())"),
            ],
        ),
        (
            "02b-integers-mod-n-as-ring",
            "Integers Mod n as a Ring",
            "Zmod(12), zero divisors, units",
            [
                ("Building Z/nZ",
                 "# Create Z/12Z and inspect basic properties\n"
                 "R = Zmod(12)\n"
                 "print('Order:', R.order())\n"
                 "print('Is field?', R.is_field())"),
                ("Zero Divisors",
                 "# Find zero divisors in Z/12Z: a*b == 0 with a,b != 0\n"
                 "R = Zmod(12)\n"
                 "for a in R:\n"
                 "    for b in R:\n"
                 "        if a != 0 and b != 0 and a*b == 0:\n"
                 "            print(f'{a} * {b} = 0')"),
                ("Units and the Unit Group",
                 "# The units of Z/12Z form a group under multiplication\n"
                 "R = Zmod(12)\n"
                 "units = [x for x in R if gcd(ZZ(x), 12) == 1]\n"
                 "print('Units:', units)"),
            ],
        ),
        (
            "02c-polynomial-rings",
            "Polynomial Rings",
            "PolynomialRing(), degree, evaluation",
            [
                ("Creating Polynomial Rings",
                 "# Build a polynomial ring over the rationals\n"
                 "R.<x> = PolynomialRing(QQ)\n"
                 "f = x^3 - 2*x + 1\n"
                 "print(f, 'degree:', f.degree())"),
                ("Polynomial Arithmetic",
                 "# Add, multiply, and divide polynomials\n"
                 "R.<x> = PolynomialRing(QQ)\n"
                 "f = x^2 + 1\n"
                 "g = x - 1\n"
                 "print('f*g =', f*g)\n"
                 "print('divmod:', f.quo_rem(g))"),
                ("Evaluation and Roots",
                 "# Evaluate a polynomial and find its roots\n"
                 "R.<x> = PolynomialRing(QQ)\n"
                 "f = x^2 - 5*x + 6\n"
                 "print('f(2) =', f(2))\n"
                 "print('roots:', f.roots())"),
            ],
        ),
        (
            "02d-what-is-a-field",
            "What Is a Field?",
            "Every element invertible, Z_p is field iff p prime",
            [
                ("Field Definition",
                 "# A field is a commutative ring where every nonzero element is a unit\n"
                 "F = GF(7)\n"
                 "print('Is field?', F.is_field())"),
                ("Z_p Is a Field When p Is Prime",
                 "# Check: Zmod(p) is a field iff p is prime\n"
                 "for n in range(2, 16):\n"
                 "    R = Zmod(n)\n"
                 "    print(f'Z/{n}Z is field: {R.is_field()}, {n} is prime: {is_prime(n)}')"),
                ("Inverses in a Prime Field",
                 "# Every nonzero element of GF(p) has a multiplicative inverse\n"
                 "F = GF(7)\n"
                 "for a in F:\n"
                 "    if a != 0:\n"
                 "        print(f'{a}^(-1) = {a^(-1)}')"),
            ],
        ),
        (
            "02e-polynomial-division-irreducibility",
            "Polynomial Division and Irreducibility",
            "divmod for polys, is_irreducible()",
            [
                ("Polynomial Long Division",
                 "# Divide f by g and get quotient + remainder\n"
                 "R.<x> = PolynomialRing(QQ)\n"
                 "f = x^4 + x^2 + 1\n"
                 "g = x^2 + x + 1\n"
                 "q, r = f.quo_rem(g)\n"
                 "print(f'q={q}, r={r}')"),
                ("Irreducibility Testing",
                 "# Check which polynomials over GF(2) are irreducible\n"
                 "R.<x> = PolynomialRing(GF(2))\n"
                 "for f in [x^2+x+1, x^2+1, x^3+x+1, x^3+x^2+1]:\n"
                 "    print(f'{f}: irreducible = {f.is_irreducible()}')"),
                ("Factoring Polynomials",
                 "# Factor polynomials over different base rings\n"
                 "R.<x> = PolynomialRing(GF(2))\n"
                 "f = x^4 + 1\n"
                 "print(f.factor())"),
            ],
        ),
        (
            "02f-quotient-rings",
            "Quotient Rings and Field Extensions",
            "quotient(), building GF(4) from F_2[x]",
            [
                ("Quotient Ring Construction",
                 "# Build GF(4) as F_2[x] / (x^2 + x + 1)\n"
                 "R.<x> = PolynomialRing(GF(2))\n"
                 "S.<a> = R.quotient(x^2 + x + 1)\n"
                 "print(list(S))"),
                ("Arithmetic in the Quotient",
                 "# Multiply elements in GF(4)\n"
                 "R.<x> = PolynomialRing(GF(2))\n"
                 "S.<a> = R.quotient(x^2 + x + 1)\n"
                 "print(f'a * (a+1) = {a * (a+1)}')"),
                ("Verifying Field Properties",
                 "# Check that our quotient ring is actually a field\n"
                 "R.<x> = PolynomialRing(GF(2))\n"
                 "S.<a> = R.quotient(x^2 + x + 1)\n"
                 "print('Is field?', S.is_field())"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # foundations/03  (6 notebooks)
    # ------------------------------------------------------------------
    "foundations/03-galois-fields-aes": [
        (
            "03a-binary-fields-gf2",
            "The Binary Field GF(2)",
            "XOR as addition, AND as multiplication",
            [
                ("GF(2): The Smallest Field",
                 "# GF(2) has only 0 and 1\n"
                 "F = GF(2)\n"
                 "print('Elements:', list(F))"),
                ("XOR Is Addition",
                 "# Addition in GF(2) is XOR\n"
                 "F = GF(2)\n"
                 "for a in F:\n"
                 "    for b in F:\n"
                 "        print(f'{a} + {b} = {a+b}')"),
                ("AND Is Multiplication",
                 "# Multiplication in GF(2) is AND\n"
                 "F = GF(2)\n"
                 "for a in F:\n"
                 "    for b in F:\n"
                 "        print(f'{a} * {b} = {a*b}')"),
            ],
        ),
        (
            "03b-extension-fields-gf2n",
            "Extension Fields GF(2^n)",
            "Building GF(2^n) from polynomial quotient rings",
            [
                ("From GF(2) to GF(2^n)",
                 "# Build GF(2^4) using an irreducible polynomial\n"
                 "F.<a> = GF(2^4)\n"
                 "print(F)\n"
                 "print('Modulus:', F.modulus())"),
                ("Elements as Polynomials",
                 "# Each element of GF(2^n) is a polynomial of degree < n\n"
                 "F.<a> = GF(2^4)\n"
                 "for x in F:\n"
                 "    print(x, '->', x.polynomial())"),
                ("Arithmetic in GF(2^n)",
                 "# Add and multiply elements\n"
                 "F.<a> = GF(2^4)\n"
                 "x = a^3 + a + 1\n"
                 "y = a^2 + a\n"
                 "print(f'{x} + {y} = {x+y}')\n"
                 "print(f'{x} * {y} = {x*y}')"),
            ],
        ),
        (
            "03c-gf256-arithmetic",
            "Arithmetic in GF(256)",
            "AES irreducible polynomial, field operations",
            [
                ("The AES Field: GF(2^8)",
                 "# AES uses GF(2^8) with irreducible polynomial x^8 + x^4 + x^3 + x + 1\n"
                 "R.<x> = PolynomialRing(GF(2))\n"
                 "p = x^8 + x^4 + x^3 + x + 1\n"
                 "print('Irreducible?', p.is_irreducible())"),
                ("Field Operations as Byte Manipulation",
                 "# Build GF(256) with the AES polynomial\n"
                 "F.<a> = GF(2^8, modulus=x^8 + x^4 + x^3 + x + 1)\n"
                 "print('Order:', F.order())"),
                ("Inverses and the Logarithm Table",
                 "# Compute multiplicative inverses in GF(256)\n"
                 "F.<a> = GF(2^8)\n"
                 "elem = a^6 + a^4 + a + 1  # some element\n"
                 "print(f'Inverse: {elem^(-1)}')\n"
                 "print(f'Check: {elem * elem^(-1)}')"),
            ],
        ),
        (
            "03d-aes-sbox-construction",
            "The AES S-Box",
            "Multiplicative inverse + affine transform",
            [
                ("Multiplicative Inverse in GF(256)",
                 "# The first step of the S-Box: take the inverse in GF(2^8)\n"
                 "F.<a> = GF(2^8)\n"
                 "# Map byte to field element, invert, map back\n"
                 "# TODO: implement byte-to-field and field-to-byte conversion"),
                ("The Affine Transformation",
                 "# After inversion, apply a fixed affine map over GF(2)\n"
                 "# S(x) = A * x^(-1) + c  (in GF(2)^8)\n"
                 "# TODO: implement the affine matrix and constant"),
                ("Building the Full S-Box Table",
                 "# Construct the 256-entry S-Box lookup table\n"
                 "# TODO: combine inverse + affine for all 256 inputs\n"
                 "# Expected S-Box[0x00] = 0x63, S-Box[0x01] = 0x7C"),
            ],
        ),
        (
            "03e-aes-mixcolumns-as-field-ops",
            "AES MixColumns as Field Operations",
            "Column polynomial multiplication",
            [
                ("The MixColumns Matrix",
                 "# MixColumns multiplies each column by a fixed matrix in GF(2^8)\n"
                 "# Matrix entries: 02, 03, 01, 01 (circulant)\n"
                 "# TODO: define the MixColumns matrix over GF(2^8)"),
                ("Polynomial Representation",
                 "# Each column is a polynomial in GF(2^8)[x] / (x^4 + 1)\n"
                 "# MixColumns = multiply by c(x) = 03*x^3 + 01*x^2 + 01*x + 02\n"
                 "# TODO: implement polynomial multiplication mod x^4 + 1"),
                ("Step-by-Step Example",
                 "# Apply MixColumns to a sample column\n"
                 "# TODO: walk through one column transformation"),
            ],
        ),
        (
            "03f-full-aes-round",
            "A Full AES Round",
            "SubBytes + ShiftRows + MixColumns + AddRoundKey",
            [
                ("SubBytes: Byte Substitution",
                 "# Apply the S-Box to every byte of the state\n"
                 "# TODO: apply S-Box lookup to 4x4 state matrix"),
                ("ShiftRows and MixColumns",
                 "# ShiftRows: cyclic left shift of each row\n"
                 "# MixColumns: matrix multiply each column\n"
                 "# TODO: implement ShiftRows and MixColumns"),
                ("AddRoundKey and Full Round",
                 "# XOR the state with the round key\n"
                 "# TODO: combine all four operations into one AES round"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # foundations/04  (6 notebooks)
    # ------------------------------------------------------------------
    "foundations/04-number-theory-rsa": [
        (
            "04a-divisibility-gcd-euclid",
            "Divisibility and the Euclidean Algorithm",
            "gcd(), step-by-step Euclid",
            [
                ("Divisibility",
                 "# Test divisibility and list divisors\n"
                 "n = 60\n"
                 "print('Divisors of', n, ':', divisors(n))"),
                ("The Euclidean Algorithm",
                 "# Step-by-step Euclidean algorithm\n"
                 "a, b = 252, 105\n"
                 "while b != 0:\n"
                 "    print(f'{a} = {a//b}*{b} + {a%b}')\n"
                 "    a, b = b, a % b\n"
                 "print('GCD:', a)"),
                ("Using SageMath's gcd()",
                 "# Verify with SageMath's built-in\n"
                 "print(gcd(252, 105))\n"
                 "print(gcd(48, 18))"),
            ],
        ),
        (
            "04b-extended-euclidean-algorithm",
            "The Extended Euclidean Algorithm",
            "xgcd(), Bezout, mod inverse",
            [
                ("Bezout's Identity",
                 "# Find s, t such that gcd(a,b) = s*a + t*b\n"
                 "g, s, t = xgcd(252, 105)\n"
                 "print(f'gcd = {g}, s = {s}, t = {t}')\n"
                 "print(f'Verify: {s}*252 + {t}*105 = {s*252 + t*105}')"),
                ("Computing Modular Inverses",
                 "# The extended GCD gives us modular inverses\n"
                 "# Find 17^(-1) mod 43\n"
                 "g, s, _ = xgcd(17, 43)\n"
                 "print(f'17^(-1) mod 43 = {s % 43}')"),
                ("When Does an Inverse Exist?",
                 "# a has an inverse mod n iff gcd(a, n) = 1\n"
                 "n = 15\n"
                 "for a in range(1, n):\n"
                 "    g = gcd(a, n)\n"
                 "    inv = f'{inverse_mod(a, n)}' if g == 1 else 'none'\n"
                 "    print(f'{a}: gcd={g}, inverse={inv}')"),
            ],
        ),
        (
            "04c-euler-totient-fermats-theorem",
            "Euler's Totient and Fermat's Theorem",
            "euler_phi(), power_mod()",
            [
                ("Euler's Totient Function",
                 "# phi(n) counts integers 1..n coprime to n\n"
                 "for n in range(2, 21):\n"
                 "    print(f'phi({n}) = {euler_phi(n)}')"),
                ("Fermat's Little Theorem",
                 "# a^(p-1) = 1 (mod p) for prime p, gcd(a,p)=1\n"
                 "p = 17\n"
                 "for a in range(1, p):\n"
                 "    print(f'{a}^{p-1} mod {p} = {power_mod(a, p-1, p)}')"),
                ("Euler's Theorem",
                 "# a^phi(n) = 1 (mod n) when gcd(a,n)=1\n"
                 "n = 15\n"
                 "phi_n = euler_phi(n)\n"
                 "for a in range(1, n):\n"
                 "    if gcd(a, n) == 1:\n"
                 "        print(f'{a}^{phi_n} mod {n} = {power_mod(a, phi_n, n)}')"),
            ],
        ),
        (
            "04d-chinese-remainder-theorem",
            "The Chinese Remainder Theorem",
            "CRT_list(), solving congruences",
            [
                ("Simultaneous Congruences",
                 "# Solve: x = 2 mod 3, x = 3 mod 5, x = 2 mod 7\n"
                 "x = CRT_list([2, 3, 2], [3, 5, 7])\n"
                 "print(f'x = {x}')\n"
                 "print(f'Check: {x%3}, {x%5}, {x%7}')"),
                ("CRT and Isomorphism",
                 "# Z/15Z is isomorphic to Z/3Z x Z/5Z when gcd(3,5)=1\n"
                 "for x in range(15):\n"
                 "    print(f'{x} -> ({x%3}, {x%5})')"),
                ("CRT in RSA",
                 "# CRT speeds up RSA decryption by splitting mod n = p*q\n"
                 "# TODO: demonstrate CRT-based RSA decryption"),
            ],
        ),
        (
            "04e-rsa-key-generation",
            "RSA Key Generation",
            "random_prime(), step-by-step keygen",
            [
                ("Generating Large Primes",
                 "# Use random_prime() to pick primes of a given size\n"
                 "p = random_prime(2^512)\n"
                 "q = random_prime(2^512)\n"
                 "print(f'p = {p}')\n"
                 "print(f'q = {q}')"),
                ("Computing the RSA Modulus",
                 "# n = p*q, phi(n) = (p-1)*(q-1)\n"
                 "p = random_prime(2^64)\n"
                 "q = random_prime(2^64)\n"
                 "n = p * q\n"
                 "phi_n = (p-1) * (q-1)\n"
                 "print(f'n = {n}')\n"
                 "print(f'phi(n) = {phi_n}')"),
                ("Choosing e and Computing d",
                 "# e = 65537 (standard), d = e^(-1) mod phi(n)\n"
                 "e = 65537\n"
                 "# Ensure gcd(e, phi_n) == 1\n"
                 "# d = inverse_mod(e, phi_n)\n"
                 "# TODO: complete keygen and output (n, e) and (n, d)"),
            ],
        ),
        (
            "04f-rsa-encryption-decryption",
            "RSA Encryption and Decryption",
            "Encrypt/decrypt, textbook RSA limits",
            [
                ("Textbook RSA Encryption",
                 "# Encrypt: c = m^e mod n\n"
                 "# TODO: set up RSA parameters and encrypt a message"),
                ("Textbook RSA Decryption",
                 "# Decrypt: m = c^d mod n\n"
                 "# TODO: decrypt and verify we recover the original message"),
                ("Why Textbook RSA Is Insecure",
                 "# Textbook RSA is deterministic -> same plaintext = same ciphertext\n"
                 "# TODO: demonstrate the lack of semantic security"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # foundations/05  (6 notebooks)
    # ------------------------------------------------------------------
    "foundations/05-discrete-log-diffie-hellman": [
        (
            "05a-the-discrete-log-problem",
            "The Discrete Logarithm Problem",
            "Definition, brute force, discrete_log()",
            [
                ("The DLP Definition",
                 "# Given g, h in a group, find x such that g^x = h\n"
                 "p = 23\n"
                 "g = Mod(5, p)\n"
                 "x_secret = 13\n"
                 "h = g^x_secret\n"
                 "print(f'g={g}, h={h}, find x such that g^x = h')"),
                ("Brute Force Search",
                 "# Try all possible exponents (only feasible for small groups)\n"
                 "p = 23\n"
                 "g = Mod(5, p)\n"
                 "h = Mod(g^13, p)\n"
                 "for x in range(p):\n"
                 "    if g^x == h:\n"
                 "        print(f'Found: x = {x}')\n"
                 "        break"),
                ("Using discrete_log()",
                 "# SageMath's built-in DLP solver\n"
                 "p = next_prime(10^6)\n"
                 "g = Mod(primitive_root(p), p)\n"
                 "x_secret = randint(2, p-2)\n"
                 "h = g^x_secret\n"
                 "x_found = discrete_log(h, g)\n"
                 "print(f'Secret: {x_secret}, Found: {x_found}')"),
            ],
        ),
        (
            "05b-primitive-roots-generators",
            "Primitive Roots and Generators",
            "primitive_root(), generator choice",
            [
                ("Primitive Roots",
                 "# A primitive root of p generates all of (Z/pZ)*\n"
                 "p = 23\n"
                 "g = primitive_root(p)\n"
                 "print(f'Primitive root of {p}: {g}')"),
                ("Verifying a Generator",
                 "# g is a generator iff its order equals p-1\n"
                 "p = 23\n"
                 "g = Mod(5, p)\n"
                 "print(f'Order of {g}: {g.multiplicative_order()}')\n"
                 "print(f'Is generator: {g.multiplicative_order() == p-1}')"),
                ("Finding All Generators",
                 "# List all primitive roots of a prime\n"
                 "p = 23\n"
                 "gens = [g for g in range(1,p) if Mod(g,p).multiplicative_order() == p-1]\n"
                 "print(f'Generators of (Z/{p}Z)*: {gens}')"),
            ],
        ),
        (
            "05c-diffie-hellman-key-exchange",
            "Diffie-Hellman Key Exchange",
            "Full DH exchange simulation",
            [
                ("Public Parameters",
                 "# Alice and Bob agree on a prime p and generator g\n"
                 "p = next_prime(10^20)\n"
                 "g = Mod(primitive_root(p), p)\n"
                 "print(f'p = {p}')\n"
                 "print(f'g = {g}')"),
                ("Key Exchange Protocol",
                 "# Alice picks a, sends g^a; Bob picks b, sends g^b\n"
                 "a = randint(2, p-2)  # Alice's secret\n"
                 "b = randint(2, p-2)  # Bob's secret\n"
                 "A = g^a  # Alice sends this\n"
                 "B = g^b  # Bob sends this\n"
                 "print(f'Alice sends: {A}')\n"
                 "print(f'Bob sends:   {B}')"),
                ("Shared Secret",
                 "# Both compute the same shared secret\n"
                 "# Alice: B^a = g^(ba), Bob: A^b = g^(ab)\n"
                 "shared_alice = B^a\n"
                 "shared_bob = A^b\n"
                 "print(f'Alice computes: {shared_alice}')\n"
                 "print(f'Bob computes:   {shared_bob}')\n"
                 "assert shared_alice == shared_bob"),
            ],
        ),
        (
            "05d-computational-hardness-cdh-ddh",
            "CDH and DDH Assumptions",
            "Computational vs decisional hardness",
            [
                ("The CDH Assumption",
                 "# Given g, g^a, g^b, it is hard to compute g^(ab)\n"
                 "# This is what makes Diffie-Hellman secure\n"
                 "p = next_prime(10^20)\n"
                 "g = Mod(primitive_root(p), p)\n"
                 "a, b = randint(2, p-2), randint(2, p-2)\n"
                 "print(f'g^a = {g^a}')\n"
                 "print(f'g^b = {g^b}')\n"
                 "print(f'g^(ab) = {g^(a*b)}  <- hard to compute without a or b')"),
                ("The DDH Assumption",
                 "# Given g, g^a, g^b, g^c: is c = ab mod (p-1)?\n"
                 "# DDH says this is indistinguishable from random\n"
                 "# TODO: create DDH challenge and random tuples for comparison"),
                ("Relationship Between Assumptions",
                 "# DDH => CDH => DLP (each implies the next)\n"
                 "# If you can solve DLP, you can solve CDH; if CDH, then DDH\n"
                 "# TODO: illustrate the hierarchy with examples"),
            ],
        ),
        (
            "05e-baby-step-giant-step",
            "Baby-Step Giant-Step Algorithm",
            "O(sqrt(n)), table visualization",
            [
                ("The Idea: Time-Space Tradeoff",
                 "# Split x = i*m + j where m = ceil(sqrt(n))\n"
                 "# Baby steps: compute g^j for j=0..m-1\n"
                 "# Giant steps: compute h*g^(-im) for i=0..m-1\n"
                 "# Match gives x\n"
                 "p = 101\n"
                 "n = p - 1  # group order\n"
                 "m = isqrt(n) + 1\n"
                 "print(f'Group order: {n}, step size m: {m}')"),
                ("Building the Baby-Step Table",
                 "# Compute and store g^j for j = 0, 1, ..., m-1\n"
                 "g = Mod(primitive_root(p), p)\n"
                 "baby = {}\n"
                 "gj = Mod(1, p)\n"
                 "for j in range(m):\n"
                 "    baby[gj] = j\n"
                 "    gj *= g\n"
                 "print(f'Baby-step table has {len(baby)} entries')"),
                ("Giant Steps and Matching",
                 "# Compute h * g^(-im) and look for a match\n"
                 "h = g^42  # target\n"
                 "g_inv_m = g^(-m)\n"
                 "gamma = h\n"
                 "for i in range(m):\n"
                 "    if gamma in baby:\n"
                 "        x = i*m + baby[gamma]\n"
                 "        print(f'Found x = {x}')\n"
                 "        break\n"
                 "    gamma *= g_inv_m"),
            ],
        ),
        (
            "05f-pohlig-hellman",
            "The Pohlig-Hellman Algorithm",
            "Factor order, subgroup DLPs, CRT combination",
            [
                ("Why Group Order Matters",
                 "# If |G| has small prime factors, DLP is easier\n"
                 "p = 433  # p-1 = 432 = 2^4 * 3^3\n"
                 "print(f'p-1 = {p-1}')\n"
                 "print(f'Factorization: {factor(p-1)}')"),
                ("Solving DLP in Subgroups",
                 "# Reduce to DLP in each prime-order subgroup\n"
                 "# For each prime power q^e dividing |G|:\n"
                 "#   compute x mod q^e by projecting into subgroup of order q^e\n"
                 "# TODO: implement subgroup projection"),
                ("CRT Combination",
                 "# Combine sub-results using CRT to recover full x\n"
                 "# TODO: combine the subgroup DLP solutions with CRT_list()"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # foundations/06  (6 notebooks)
    # ------------------------------------------------------------------
    "foundations/06-elliptic-curves": [
        (
            "06a-curves-over-reals",
            "Elliptic Curves over the Reals",
            "Plotting y^2 = x^3 + ax + b",
            [
                ("The Weierstrass Equation",
                 "# An elliptic curve: y^2 = x^3 + ax + b\n"
                 "# The discriminant must be nonzero: 4a^3 + 27b^2 != 0\n"
                 "a, b = -1, 1\n"
                 "print(f'Discriminant: {4*a^3 + 27*b^2}')"),
                ("Plotting Curves",
                 "# Plot an elliptic curve over the reals\n"
                 "E = EllipticCurve(RR, [-1, 1])\n"
                 "E.plot()"),
                ("Varying Parameters",
                 "# Explore how a and b affect the curve shape\n"
                 "# TODO: plot several curves with different a, b values"),
            ],
        ),
        (
            "06b-point-addition-geometry",
            "Point Addition: The Geometry",
            "Chord-and-tangent, point at infinity",
            [
                ("The Chord-and-Tangent Rule",
                 "# To add P + Q: draw line through P and Q, find third intersection, reflect\n"
                 "E = EllipticCurve(QQ, [-1, 1])\n"
                 "P = E(0, 1)\n"
                 "Q = E(1, 1)\n"
                 "print(f'P + Q = {P + Q}')"),
                ("The Point at Infinity",
                 "# The identity element: O (point at infinity)\n"
                 "E = EllipticCurve(QQ, [-1, 1])\n"
                 "P = E(0, 1)\n"
                 "O = E(0)  # point at infinity\n"
                 "print(f'P + O = {P + O}')"),
                ("Point Doubling",
                 "# When P = Q, use the tangent line\n"
                 "E = EllipticCurve(QQ, [-1, 1])\n"
                 "P = E(0, 1)\n"
                 "print(f'2*P = {2*P}')"),
            ],
        ),
        (
            "06c-curves-over-finite-fields",
            "Curves over Finite Fields",
            "EllipticCurve(GF(p),[a,b]), points()",
            [
                ("Defining a Curve over GF(p)",
                 "# Create an elliptic curve over a prime field\n"
                 "p = 23\n"
                 "E = EllipticCurve(GF(p), [1, 1])\n"
                 "print(E)"),
                ("Listing All Points",
                 "# Enumerate every point on the curve\n"
                 "p = 23\n"
                 "E = EllipticCurve(GF(p), [1, 1])\n"
                 "pts = E.points()\n"
                 "print(f'{len(pts)} points (including O)')\n"
                 "for P in pts:\n"
                 "    print(P)"),
                ("Point Arithmetic over GF(p)",
                 "# Addition and scalar multiplication work the same way\n"
                 "p = 23\n"
                 "E = EllipticCurve(GF(p), [1, 1])\n"
                 "P = E.random_point()\n"
                 "Q = E.random_point()\n"
                 "print(f'P = {P}')\n"
                 "print(f'Q = {Q}')\n"
                 "print(f'P + Q = {P + Q}')"),
            ],
        ),
        (
            "06d-group-structure-and-order",
            "Group Structure and Order",
            "E.order(), Hasse bound, abelian_group()",
            [
                ("Counting Points: Hasse's Theorem",
                 "# |E(GF(p))| is close to p+1: |#E - (p+1)| <= 2*sqrt(p)\n"
                 "p = 101\n"
                 "E = EllipticCurve(GF(p), [1, 1])\n"
                 "n = E.order()\n"
                 "print(f'#E = {n}, p+1 = {p+1}, bound = {2*isqrt(p)}')"),
                ("Group Structure",
                 "# The group E(GF(p)) is isomorphic to Z/n1 x Z/n2\n"
                 "p = 101\n"
                 "E = EllipticCurve(GF(p), [1, 1])\n"
                 "print(E.abelian_group())"),
                ("Point Orders",
                 "# Find the order of individual points\n"
                 "p = 101\n"
                 "E = EllipticCurve(GF(p), [1, 1])\n"
                 "P = E.random_point()\n"
                 "print(f'Order of P: {P.order()}')"),
            ],
        ),
        (
            "06e-scalar-multiplication",
            "Scalar Multiplication",
            "Double-and-add, n*P",
            [
                ("Repeated Addition",
                 "# n*P means P + P + ... + P (n times)\n"
                 "E = EllipticCurve(GF(101), [1, 1])\n"
                 "P = E.random_point()\n"
                 "print(f'P = {P}')\n"
                 "print(f'5*P = {5*P}')"),
                ("Double-and-Add Algorithm",
                 "# Efficient scalar multiplication using binary expansion of n\n"
                 "def double_and_add(P, n):\n"
                 "    R = P.curve()(0)  # point at infinity\n"
                 "    Q = P\n"
                 "    while n > 0:\n"
                 "        if n % 2 == 1:\n"
                 "            R = R + Q\n"
                 "        Q = Q + Q\n"
                 "        n = n // 2\n"
                 "    return R\n"
                 "# TODO: test against SageMath's built-in n*P"),
                ("The ECDLP",
                 "# Given P and Q = n*P, finding n is the ECDLP\n"
                 "E = EllipticCurve(GF(101), [1, 1])\n"
                 "P = E.random_point()\n"
                 "n_secret = randint(1, P.order()-1)\n"
                 "Q = n_secret * P\n"
                 "print(f'P = {P}, Q = {Q}')\n"
                 "print(f'Can you find n such that Q = n*P?')"),
            ],
        ),
        (
            "06f-ecdh-and-ecdsa",
            "ECDH and ECDSA",
            "Key exchange and signatures on curves",
            [
                ("ECDH Key Exchange",
                 "# Same Diffie-Hellman idea, but on an elliptic curve\n"
                 "E = EllipticCurve(GF(next_prime(10^6)), [1, 1])\n"
                 "P = E.random_point()\n"
                 "n = P.order()\n"
                 "a = randint(1, n-1)  # Alice's secret\n"
                 "b = randint(1, n-1)  # Bob's secret\n"
                 "A = a * P  # Alice's public\n"
                 "B = b * P  # Bob's public\n"
                 "print(f'Shared secret match: {a*B == b*A}')"),
                ("ECDSA Signing",
                 "# Sign a message hash with ECDSA\n"
                 "# TODO: implement ECDSA signing step by step"),
                ("ECDSA Verification",
                 "# Verify an ECDSA signature\n"
                 "# TODO: implement ECDSA verification step by step"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # frontier/07  (5 notebooks)
    # ------------------------------------------------------------------
    "frontier/07-pairings": [
        (
            "07a-bilinear-maps-definition",
            "Bilinear Maps",
            "e: G1 x G2 -> GT, bilinearity property",
            [
                ("What Is a Bilinear Map?",
                 "# A pairing e: G1 x G2 -> GT satisfying\n"
                 "# e(aP, bQ) = e(P, Q)^(ab)\n"
                 "# TODO: set up pairing-friendly curve in SageMath"),
                ("The Bilinearity Property",
                 "# Verify: e(P+P', Q) = e(P,Q) * e(P',Q)\n"
                 "# TODO: demonstrate bilinearity with concrete examples"),
                ("Non-Degeneracy",
                 "# If P != O and Q != O, then e(P, Q) != 1\n"
                 "# TODO: check non-degeneracy condition"),
            ],
        ),
        (
            "07b-weil-pairing-intuition",
            "The Weil Pairing",
            "Divisors intro, weil_pairing()",
            [
                ("Divisors on Curves",
                 "# A divisor is a formal sum of points on the curve\n"
                 "# TODO: introduce divisors with simple examples"),
                ("Computing the Weil Pairing",
                 "# SageMath's weil_pairing() for torsion points\n"
                 "# TODO: compute Weil pairing on a small curve"),
                ("Properties of the Weil Pairing",
                 "# Alternating: e(P, P) = 1\n"
                 "# TODO: verify key properties of the Weil pairing"),
            ],
        ),
        (
            "07c-pairing-friendly-curves",
            "Pairing-Friendly Curves",
            "BN curves, embedding degree",
            [
                ("Embedding Degree",
                 "# The embedding degree k is the smallest k with r | p^k - 1\n"
                 "# TODO: compute embedding degree for sample curves"),
                ("BN Curves",
                 "# Barreto-Naehrig curves: pairing-friendly with embedding degree 12\n"
                 "# TODO: parameterize a BN curve"),
                ("Security Considerations",
                 "# Embedding degree affects both efficiency and security\n"
                 "# TODO: discuss the relationship between k and security level"),
            ],
        ),
        (
            "07d-bls-signatures",
            "BLS Signatures",
            "Sign, verify, aggregate",
            [
                ("BLS Signature Scheme",
                 "# Sign: sigma = sk * H(m)  (hash to curve point)\n"
                 "# Verify: e(sigma, g2) == e(H(m), pk)\n"
                 "# TODO: implement BLS sign and verify"),
                ("Signature Aggregation",
                 "# Multiple signatures can be aggregated into one\n"
                 "# sigma_agg = sigma_1 + sigma_2 + ... + sigma_n\n"
                 "# TODO: demonstrate signature aggregation"),
            ],
        ),
        (
            "07e-identity-based-encryption",
            "Identity-Based Encryption",
            "Boneh-Franklin IBE overview",
            [
                ("IBE Concept",
                 "# Public key = identity string (e.g., email address)\n"
                 "# A trusted authority derives private keys from a master secret\n"
                 "# TODO: outline the Boneh-Franklin IBE scheme"),
                ("Setup and Key Extraction",
                 "# Setup: master secret s, public params (P, sP)\n"
                 "# Extract: private key = s * H(ID)\n"
                 "# TODO: implement setup and key extraction"),
                ("Encrypt and Decrypt",
                 "# Encrypt to an identity; only the extracted key can decrypt\n"
                 "# TODO: demonstrate encryption and decryption"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # frontier/08  (6 notebooks)
    # ------------------------------------------------------------------
    "frontier/08-lattices-post-quantum": [
        (
            "08a-lattices-and-bases",
            "Lattices and Bases",
            "2D visualization, basis vectors, LLL()",
            [
                ("What Is a Lattice?",
                 "# A lattice is the set of all integer linear combinations of basis vectors\n"
                 "B = matrix(ZZ, [[1, 0], [0, 1]])\n"
                 "print('Basis:\\n', B)"),
                ("Visualizing a 2D Lattice",
                 "# Plot lattice points generated by a basis\n"
                 "B = matrix(ZZ, [[3, 1], [1, 2]])\n"
                 "# TODO: plot lattice points as dots in the plane"),
                ("Different Bases, Same Lattice",
                 "# Two bases generate the same lattice iff they differ by a unimodular matrix\n"
                 "B1 = matrix(ZZ, [[3, 1], [1, 2]])\n"
                 "U = matrix(ZZ, [[1, 1], [0, 1]])  # unimodular: det = +/- 1\n"
                 "B2 = U * B1\n"
                 "print('B2:\\n', B2)\n"
                 "print('det(U):', det(U))"),
            ],
        ),
        (
            "08b-shortest-vector-problem",
            "The Shortest Vector Problem",
            "SVP, good vs bad bases",
            [
                ("SVP Definition",
                 "# Find the shortest nonzero vector in a lattice\n"
                 "# This is NP-hard in general\n"
                 "B = matrix(ZZ, [[1, 0], [0, 1]])\n"
                 "L = B.LLL()\n"
                 "print('Reduced basis:\\n', L)"),
                ("Good Bases vs Bad Bases",
                 "# A 'good' basis has short, nearly orthogonal vectors\n"
                 "# A 'bad' basis has long, nearly parallel vectors\n"
                 "# TODO: compare a good and bad basis for the same lattice"),
                ("Approximating SVP",
                 "# LLL gives a vector within 2^(n/2) of the shortest\n"
                 "B = matrix(ZZ, [[1, 0, 3], [0, 1, 5], [0, 0, 7]])\n"
                 "L = B.LLL()\n"
                 "print('LLL-reduced basis:\\n', L)\n"
                 "print('Short vector:', L[0])"),
            ],
        ),
        (
            "08c-lll-algorithm",
            "The LLL Algorithm",
            "Step-by-step on 2D, reduction quality",
            [
                ("Gram-Schmidt Orthogonalization",
                 "# LLL starts with Gram-Schmidt (but keeps integer coefficients)\n"
                 "B = matrix(QQ, [[3, 1], [2, 3]])\n"
                 "G, mu = B.gram_schmidt()\n"
                 "print('Gram-Schmidt basis:\\n', G)"),
                ("The LLL Conditions",
                 "# 1) Size-reduced: |mu_{i,j}| <= 1/2\n"
                 "# 2) Lovasz condition: delta * ||b*_i||^2 <= ||b*_{i+1} + mu * b*_i||^2\n"
                 "# TODO: check LLL conditions step by step"),
                ("Running LLL",
                 "# Apply LLL to a badly-conditioned basis\n"
                 "B = matrix(ZZ, [[201, 37], [1648, 297]])\n"
                 "print('Before LLL:\\n', B)\n"
                 "L = B.LLL()\n"
                 "print('After LLL:\\n', L)"),
            ],
        ),
        (
            "08d-learning-with-errors",
            "Learning With Errors",
            "LWE definition, noise, search vs decision",
            [
                ("The LWE Problem",
                 "# Given (A, b = A*s + e mod q), find s\n"
                 "# A is random, s is secret, e is small noise\n"
                 "n, q = 5, 101\n"
                 "A = random_matrix(Zmod(q), 10, n)\n"
                 "s = random_vector(Zmod(q), n)\n"
                 "print('A:\\n', A)\n"
                 "print('s:', s)"),
                ("The Role of Noise",
                 "# Without noise: b = A*s is easy to solve (linear algebra)\n"
                 "# With noise: b = A*s + e becomes hard\n"
                 "# TODO: compare solving with and without noise"),
                ("Search-LWE vs Decision-LWE",
                 "# Search: find s from (A, b)\n"
                 "# Decision: distinguish (A, A*s+e) from (A, random)\n"
                 "# These are polynomially equivalent\n"
                 "# TODO: illustrate the search vs decision variants"),
            ],
        ),
        (
            "08e-ring-lwe",
            "Ring-LWE",
            "Polynomial ring setting, efficiency, NTRU",
            [
                ("From LWE to Ring-LWE",
                 "# Replace random matrix A with structured (polynomial) matrix\n"
                 "# Work in R_q = Z_q[x] / (x^n + 1)\n"
                 "# TODO: set up the polynomial ring R_q"),
                ("Efficiency Gains",
                 "# Ring structure allows O(n log n) operations via NTT\n"
                 "# Key size: O(n) instead of O(n^2)\n"
                 "# TODO: compare key sizes for LWE vs Ring-LWE"),
                ("Connection to NTRU",
                 "# NTRU: one of the earliest lattice-based schemes\n"
                 "# Uses similar polynomial ring structure\n"
                 "# TODO: sketch the NTRU encryption scheme"),
            ],
        ),
        (
            "08f-kyber-overview",
            "Kyber / ML-KEM Overview",
            "Module-LWE, parameters, KEM flow",
            [
                ("Module-LWE",
                 "# Kyber uses Module-LWE: matrices of ring elements\n"
                 "# Compromise between LWE generality and Ring-LWE efficiency\n"
                 "# TODO: illustrate the module structure"),
                ("Kyber Parameters",
                 "# Kyber-512, Kyber-768, Kyber-1024\n"
                 "# n=256, q=3329, various k values\n"
                 "# TODO: display parameter sets and security levels"),
                ("KEM: Key Encapsulation Mechanism",
                 "# KeyGen -> Encaps -> Decaps\n"
                 "# Produces a shared symmetric key\n"
                 "# TODO: outline the KEM flow"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # frontier/09  (5 notebooks)
    # ------------------------------------------------------------------
    "frontier/09-commitments-sigma-protocols": [
        (
            "09a-commitment-schemes",
            "Commitment Schemes",
            "Hiding, binding, hash commitment",
            [
                ("What Is a Commitment?",
                 "# Commit to a value without revealing it; open later\n"
                 "# Two properties: hiding (can't see value) and binding (can't change it)\n"
                 "# TODO: demonstrate with a hash-based commitment"),
                ("Hash-Based Commitment",
                 "# commit(m, r) = H(m || r)\n"
                 "# Open: reveal m and r; verifier checks hash\n"
                 "import hashlib\n"
                 "m = b'secret message'\n"
                 "r = b'random_nonce_12345'\n"
                 "commitment = hashlib.sha256(m + r).hexdigest()\n"
                 "print(f'Commitment: {commitment}')"),
                ("Hiding vs Binding",
                 "# Perfectly hiding: commitment reveals zero info about m\n"
                 "# Perfectly binding: cannot open to a different m'\n"
                 "# Hash commitments: computationally hiding AND binding\n"
                 "# TODO: discuss the tradeoff"),
            ],
        ),
        (
            "09b-pedersen-commitments",
            "Pedersen Commitments",
            "C = g^m * h^r, homomorphic, perfect hiding",
            [
                ("Pedersen Commitment Scheme",
                 "# Setup: group G of prime order q, generators g, h\n"
                 "# Commit: C = g^m * h^r\n"
                 "# Open: reveal m, r\n"
                 "p = next_prime(10^20)\n"
                 "g = Mod(primitive_root(p), p)\n"
                 "# h should be chosen so that log_g(h) is unknown\n"
                 "# TODO: set up Pedersen parameters"),
                ("Homomorphic Property",
                 "# C1 * C2 = g^(m1+m2) * h^(r1+r2)\n"
                 "# Commitments can be added without opening!\n"
                 "# TODO: demonstrate homomorphic addition"),
                ("Perfect Hiding",
                 "# For any m, the commitment C is uniformly random\n"
                 "# (because r is random and h^r is uniform)\n"
                 "# TODO: illustrate that different r values produce uniform C"),
            ],
        ),
        (
            "09c-sigma-protocols-intuition",
            "Sigma Protocols",
            "3-move structure, soundness, ZK",
            [
                ("The 3-Move Structure",
                 "# Prover -> Verifier: commitment (a)\n"
                 "# Verifier -> Prover: challenge (e)\n"
                 "# Prover -> Verifier: response (z)\n"
                 "# TODO: diagram the 3-move protocol"),
                ("Soundness",
                 "# A cheating prover cannot answer two different challenges\n"
                 "# Special soundness: from two accepting transcripts, extract witness\n"
                 "# TODO: illustrate soundness extraction"),
                ("Zero-Knowledge Property",
                 "# The verifier learns nothing beyond the statement's truth\n"
                 "# Simulator: can produce valid-looking transcripts without the witness\n"
                 "# TODO: demonstrate the simulation argument"),
            ],
        ),
        (
            "09d-schnorr-protocol",
            "The Schnorr Protocol",
            "Interactive Schnorr, completeness/soundness/ZK",
            [
                ("Protocol Description",
                 "# Prover knows x such that h = g^x\n"
                 "# 1. Prover picks random r, sends a = g^r\n"
                 "# 2. Verifier sends random challenge e\n"
                 "# 3. Prover sends z = r + e*x\n"
                 "# Verify: g^z == a * h^e\n"
                 "# TODO: implement the interactive protocol"),
                ("Completeness",
                 "# An honest prover always convinces the verifier\n"
                 "# g^z = g^(r + ex) = g^r * g^(ex) = a * h^e\n"
                 "# TODO: verify completeness with a concrete example"),
                ("Soundness and Zero-Knowledge",
                 "# Special soundness: two transcripts -> extract x\n"
                 "# ZK: simulator picks z, e first, computes a = g^z / h^e\n"
                 "# TODO: implement the simulator"),
            ],
        ),
        (
            "09e-fiat-shamir-transform",
            "The Fiat-Shamir Transform",
            "Hash-based challenge, non-interactive",
            [
                ("From Interactive to Non-Interactive",
                 "# Replace verifier's random challenge with a hash\n"
                 "# e = H(g, h, a)\n"
                 "# Now the prover can compute everything alone\n"
                 "# TODO: implement the Fiat-Shamir transform for Schnorr"),
                ("Non-Interactive Proof",
                 "# Proof = (a, z) where e = H(g, h, a) and z = r + e*x\n"
                 "# Verifier recomputes e from a and checks g^z == a * h^e\n"
                 "# TODO: implement non-interactive prove and verify"),
                ("Security in the Random Oracle Model",
                 "# Fiat-Shamir is secure when H behaves as a random oracle\n"
                 "# In practice, use a cryptographic hash (SHA-256, etc.)\n"
                 "# TODO: discuss random oracle model assumptions"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # frontier/10  (6 notebooks)
    # ------------------------------------------------------------------
    "frontier/10-snarks-starks": [
        (
            "10a-arithmetic-circuits",
            "Arithmetic Circuits",
            "Addition/multiplication gates, wire values",
            [
                ("What Is an Arithmetic Circuit?",
                 "# A DAG of addition and multiplication gates over a field\n"
                 "# Inputs -> gates -> output\n"
                 "# TODO: define a simple circuit: f(x) = x^3 + x + 5"),
                ("Wire Values and Evaluation",
                 "# Assign values to input wires, propagate through gates\n"
                 "# TODO: trace wire values for f(3) = 27 + 3 + 5 = 35"),
                ("Flattening to Gates",
                 "# Any computation can be flattened to a sequence of gates\n"
                 "# x^3 + x + 5:\n"
                 "#   w1 = x * x\n"
                 "#   w2 = w1 * x\n"
                 "#   w3 = w2 + x\n"
                 "#   w4 = w3 + 5\n"
                 "# TODO: implement flattening"),
            ],
        ),
        (
            "10b-r1cs-constraints",
            "R1CS Constraints",
            "A*s . B*s = C*s, flattening, witness",
            [
                ("Rank-1 Constraint System",
                 "# Each gate becomes a constraint: (A_i . s) * (B_i . s) = (C_i . s)\n"
                 "# s = (1, x, w1, w2, ..., output) is the witness vector\n"
                 "# TODO: build R1CS matrices for x^3 + x + 5"),
                ("The Witness",
                 "# The witness includes all intermediate wire values\n"
                 "# s = [1, x, x*x, x*x*x, x*x*x+x, x*x*x+x+5]\n"
                 "# TODO: construct witness for a given input"),
                ("Checking Satisfiability",
                 "# Verify that A*s . B*s == C*s for all constraints\n"
                 "# TODO: programmatically verify the R1CS"),
            ],
        ),
        (
            "10c-qap-construction",
            "QAP Construction",
            "Lagrange interpolation, vanishing polynomial",
            [
                ("From R1CS to QAP",
                 "# Interpolate each column of A, B, C into polynomials\n"
                 "# Using Lagrange interpolation at points 1, 2, ..., m\n"
                 "# TODO: convert R1CS matrices to QAP polynomials"),
                ("The Vanishing Polynomial",
                 "# Z(x) = (x-1)(x-2)...(x-m) vanishes at all constraint points\n"
                 "# Valid witness => A(x)*B(x) - C(x) = H(x)*Z(x)\n"
                 "# TODO: compute Z(x) and verify the QAP equation"),
                ("Why QAP?",
                 "# QAP allows checking all constraints with a single polynomial identity\n"
                 "# Schwartz-Zippel: check at a random point\n"
                 "# TODO: demonstrate the probabilistic check"),
            ],
        ),
        (
            "10d-groth16-overview",
            "Groth16 Overview",
            "Trusted setup, CRS, proof/verify",
            [
                ("Trusted Setup",
                 "# Generate a CRS (Common Reference String) from toxic waste tau\n"
                 "# CRS = (g^1, g^tau, g^(tau^2), ..., ...)\n"
                 "# Toxic waste must be destroyed!\n"
                 "# TODO: illustrate CRS generation"),
                ("Proof Generation",
                 "# Prover uses CRS and witness to compute proof (A, B, C)\n"
                 "# Three group elements = constant-size proof!\n"
                 "# TODO: outline the Groth16 prover"),
                ("Verification",
                 "# Verify with a single pairing equation\n"
                 "# e(A, B) = e(alpha, beta) * e(C, delta) * e(public_input_term, gamma)\n"
                 "# TODO: outline the Groth16 verifier"),
            ],
        ),
        (
            "10e-fri-protocol",
            "The FRI Protocol",
            "Polynomial commitment, folding, Reed-Solomon",
            [
                ("Reed-Solomon Codes",
                 "# A low-degree polynomial evaluated on a domain forms a codeword\n"
                 "# FRI proves that a function is close to a low-degree polynomial\n"
                 "# TODO: demonstrate Reed-Solomon encoding"),
                ("The Folding Technique",
                 "# Split f(x) into even and odd parts, combine with random challenge\n"
                 "# f(x) = f_even(x^2) + x * f_odd(x^2)\n"
                 "# New polynomial has half the degree\n"
                 "# TODO: implement one round of FRI folding"),
                ("FRI as Polynomial Commitment",
                 "# Repeated folding until constant polynomial\n"
                 "# Verifier checks consistency with Merkle proofs\n"
                 "# TODO: outline the full FRI protocol"),
            ],
        ),
        (
            "10f-starks-vs-snarks",
            "STARKs vs SNARKs",
            "Trust, proof size, verification comparison",
            [
                ("Trusted Setup vs Transparency",
                 "# SNARKs (Groth16): require trusted setup\n"
                 "# STARKs: transparent, no trusted setup needed\n"
                 "# TODO: compare trust assumptions"),
                ("Proof Size and Verification Time",
                 "# Groth16: ~200 bytes, O(1) verification\n"
                 "# STARKs: ~100 KB, O(log^2 n) verification\n"
                 "# TODO: tabulate the comparison"),
                ("When to Use Which",
                 "# SNARKs: on-chain verification (small proofs matter)\n"
                 "# STARKs: post-quantum security, no trust needed\n"
                 "# TODO: discuss practical tradeoffs"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # frontier/11  (5 notebooks)
    # ------------------------------------------------------------------
    "frontier/11-homomorphic-encryption": [
        (
            "11a-what-is-fhe",
            "What Is Fully Homomorphic Encryption?",
            "Enc(a) op Enc(b) = Enc(a op b)",
            [
                ("The FHE Dream",
                 "# Compute on encrypted data without decrypting\n"
                 "# Enc(a) + Enc(b) = Enc(a + b)\n"
                 "# Enc(a) * Enc(b) = Enc(a * b)\n"
                 "# TODO: illustrate with a toy example"),
                ("Generations of FHE",
                 "# Gen 1: Gentry (2009) - bootstrapping\n"
                 "# Gen 2: BGV, BFV - batching, modulus switching\n"
                 "# Gen 3: GSW - approximate eigenvector\n"
                 "# Gen 4: CKKS - approximate arithmetic\n"
                 "# TODO: timeline visualization"),
                ("The Noise Problem",
                 "# Each operation adds noise to the ciphertext\n"
                 "# Too much noise -> decryption fails\n"
                 "# Bootstrapping: homomorphically evaluate decryption to reduce noise\n"
                 "# TODO: demonstrate noise growth"),
            ],
        ),
        (
            "11b-partially-homomorphic-schemes",
            "Partially Homomorphic Schemes",
            "RSA mul, Paillier add, ElGamal",
            [
                ("RSA: Multiplicatively Homomorphic",
                 "# Enc(m1) * Enc(m2) = (m1^e * m2^e) mod n = (m1*m2)^e mod n = Enc(m1*m2)\n"
                 "# TODO: demonstrate with textbook RSA"),
                ("Paillier: Additively Homomorphic",
                 "# Enc(m1) * Enc(m2) = Enc(m1 + m2) in Paillier\n"
                 "# TODO: implement Paillier encryption and demonstrate addition"),
                ("ElGamal: Multiplicatively Homomorphic",
                 "# (g^r1, m1*h^r1) * (g^r2, m2*h^r2) = (g^(r1+r2), m1*m2*h^(r1+r2))\n"
                 "# TODO: demonstrate with ElGamal"),
            ],
        ),
        (
            "11c-bgv-scheme",
            "The BGV Scheme",
            "RLWE-based, modulus switching, noise",
            [
                ("BGV Encryption",
                 "# Plaintext in R_t = Z_t[x]/(x^n+1)\n"
                 "# Ciphertext in R_q = Z_q[x]/(x^n+1)\n"
                 "# ct = (b, a) where b = a*s + t*e + m\n"
                 "# TODO: implement basic BGV encryption"),
                ("Modulus Switching",
                 "# Scale ciphertext from modulus q to smaller q'\n"
                 "# This reduces noise at the cost of modulus size\n"
                 "# TODO: demonstrate modulus switching"),
                ("Homomorphic Operations",
                 "# Addition: add ciphertexts component-wise\n"
                 "# Multiplication: tensor product + relinearization\n"
                 "# TODO: implement add and multiply"),
            ],
        ),
        (
            "11d-bfv-scheme",
            "The BFV Scheme",
            "Scale-and-round, plaintext/ciphertext modulus",
            [
                ("BFV vs BGV",
                 "# BFV: noise is in the LSBs (scale-and-round)\n"
                 "# BGV: noise is in the MSBs (modulus switching)\n"
                 "# BFV is simpler for integer arithmetic\n"
                 "# TODO: compare the two approaches"),
                ("BFV Encryption",
                 "# Encode plaintext m as floor(q/t) * m + noise\n"
                 "# Decrypt: round(t * ct / q) mod t\n"
                 "# TODO: implement BFV encode/encrypt/decrypt"),
                ("Noise Budget",
                 "# Each operation consumes noise budget\n"
                 "# When budget reaches zero, decryption fails\n"
                 "# TODO: track noise budget through operations"),
            ],
        ),
        (
            "11e-ckks-approximate-arithmetic",
            "CKKS: Approximate Arithmetic",
            "Encoding reals, rescaling",
            [
                ("Encoding Real Numbers",
                 "# CKKS encodes real/complex numbers into polynomials\n"
                 "# Encode: scale by Delta, round to integer polynomial\n"
                 "# Decode: divide by Delta\n"
                 "# TODO: implement CKKS encoding"),
                ("Rescaling",
                 "# After multiplication, scale grows: Delta^2\n"
                 "# Rescale: divide ciphertext by Delta to get back to Delta\n"
                 "# This is the key innovation of CKKS\n"
                 "# TODO: demonstrate rescaling"),
                ("Approximate Computations",
                 "# CKKS allows small errors in the result\n"
                 "# Perfect for ML inference, statistics, signal processing\n"
                 "# TODO: compute a simple function on encrypted reals"),
            ],
        ),
    ],

    # ------------------------------------------------------------------
    # frontier/12  (5 notebooks)
    # ------------------------------------------------------------------
    "frontier/12-mpc": [
        (
            "12a-secret-sharing-shamir",
            "Shamir Secret Sharing",
            "Polynomial interpolation, t-of-n",
            [
                ("The Idea: Hide a Secret in a Polynomial",
                 "# Secret s is the constant term of a random degree-(t-1) polynomial\n"
                 "# Share i = f(i) for i = 1, 2, ..., n\n"
                 "R.<x> = PolynomialRing(GF(next_prime(1000)))\n"
                 "# TODO: construct a random polynomial with secret as f(0)"),
                ("Sharing",
                 "# Evaluate the polynomial at n distinct points\n"
                 "# Any t shares can reconstruct; fewer than t reveal nothing\n"
                 "# TODO: generate n shares from the polynomial"),
                ("Reconstruction via Lagrange Interpolation",
                 "# Given t shares (x_i, y_i), interpolate to recover f(0)\n"
                 "# TODO: use Lagrange interpolation to reconstruct the secret"),
            ],
        ),
        (
            "12b-secret-sharing-additive",
            "Additive Secret Sharing",
            "Random splits, XOR, reconstruction",
            [
                ("Additive Sharing over a Field",
                 "# Split secret s into n shares: s = s_1 + s_2 + ... + s_n\n"
                 "# Pick s_1, ..., s_{n-1} randomly; s_n = s - sum(others)\n"
                 "# TODO: implement additive sharing"),
                ("XOR-Based Sharing",
                 "# For binary data: s = s_1 XOR s_2 XOR ... XOR s_n\n"
                 "# TODO: implement XOR sharing and reconstruction"),
                ("Addition on Shared Values",
                 "# To add shared values: each party adds their shares locally\n"
                 "# [a] + [b] = [a+b] without any communication!\n"
                 "# TODO: demonstrate local addition on shares"),
            ],
        ),
        (
            "12c-yaos-garbled-circuits",
            "Yao's Garbled Circuits",
            "Gate garbling, wire labels",
            [
                ("Wire Labels",
                 "# Each wire gets two random labels: one for 0, one for 1\n"
                 "# The evaluator sees one label per wire but doesn't know which bit it represents\n"
                 "# TODO: generate random wire labels"),
                ("Garbling a Gate",
                 "# For each gate, encrypt the output label under the input labels\n"
                 "# Four entries (for AND gate): only one decrypts correctly\n"
                 "# TODO: garble an AND gate"),
                ("Evaluating the Garbled Circuit",
                 "# The evaluator decrypts one entry per gate using their wire labels\n"
                 "# Oblivious transfer provides the input labels\n"
                 "# TODO: evaluate a simple garbled circuit"),
            ],
        ),
        (
            "12d-oblivious-transfer",
            "Oblivious Transfer",
            "1-of-2 OT, sender/receiver privacy",
            [
                ("1-of-2 Oblivious Transfer",
                 "# Sender has (m0, m1); receiver has choice bit b\n"
                 "# Receiver gets m_b; sender doesn't learn b\n"
                 "# TODO: implement 1-of-2 OT using DH"),
                ("RSA-Based OT",
                 "# Classic construction using RSA blinding\n"
                 "# TODO: implement RSA-based OT"),
                ("OT Extension",
                 "# A few base OTs -> many OTs using symmetric crypto\n"
                 "# Key optimization for practical MPC\n"
                 "# TODO: outline OT extension"),
            ],
        ),
        (
            "12e-spdz-protocol",
            "The SPDZ Protocol",
            "Beaver triples, online/offline, malicious security",
            [
                ("Beaver Triples",
                 "# Pre-shared random triples (a, b, c) with c = a*b\n"
                 "# Allow multiplication on shared values\n"
                 "# TODO: demonstrate Beaver triple generation"),
                ("Online Phase: Multiplication",
                 "# To multiply [x]*[y]:\n"
                 "# Open d = x-a and e = y-b\n"
                 "# [xy] = [c] + d*[y] + e*[x] + d*e\n"
                 "# TODO: implement online multiplication"),
                ("Malicious Security",
                 "# SPDZ uses MACs to detect cheating parties\n"
                 "# Each share has an authentication tag\n"
                 "# TODO: demonstrate MAC-based verification"),
            ],
        ),
    ],
}


# ---------------------------------------------------------------------------
# SageMath kernel metadata (Jupyter v4 format)
# ---------------------------------------------------------------------------
SAGEMATH_KERNEL = {
    "kernelspec": {
        "display_name": "SageMath",
        "language": "sage",
        "name": "sagemath",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "sage",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _md_cell(source: str) -> dict:
    """Create a Jupyter markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def _code_cell(source: str) -> dict:
    """Create a Jupyter code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def _next_notebook_link(module_path: str, notebooks: list, idx: int) -> str:
    """Return a markdown 'Next' link to the following notebook, or empty str."""
    if idx + 1 < len(notebooks):
        next_stem = notebooks[idx + 1][0]
        next_title = notebooks[idx + 1][1]
        return f"\n\n**Next:** [{next_title}]({next_stem}.ipynb)"
    return ""


def _build_notebook(
    module_path: str,
    notebooks: list,
    idx: int,
    stem: str,
    title: str,
    description: str,
    sections: list[tuple[str, str]],
) -> dict:
    """Build a complete Jupyter notebook dict."""
    # Derive module number and name for display
    module_dir = Path(module_path).name  # e.g. "01-modular-arithmetic-groups"
    module_num = module_dir.split("-")[0]  # e.g. "01"

    cells: list[dict] = []

    # --- Title cell ---
    cells.append(_md_cell(
        f"# {title}\n"
        f"\n"
        f"**Module {module_num}** | {module_dir}\n"
        f"\n"
        f"*{description}*"
    ))

    # --- Objectives cell ---
    cells.append(_md_cell(
        f"## Objectives\n"
        f"\n"
        f"By the end of this notebook you will be able to:\n"
        f"\n"
        f"1. Understand the core ideas behind **{title.lower()}**.\n"
        f"2. Explore these concepts interactively using SageMath.\n"
        f"3. Build intuition through hands-on computation and visualization."
    ))

    # --- Prerequisites cell ---
    if idx == 0:
        prereq_text = (
            "## Prerequisites\n"
            "\n"
            "- Basic familiarity with Python syntax.\n"
            "- A working SageMath installation (or access to CoCalc/SageMathCell)."
        )
    else:
        prev_stem = notebooks[idx - 1][0]
        prev_title = notebooks[idx - 1][1]
        prereq_text = (
            "## Prerequisites\n"
            "\n"
            f"- Completion of [{prev_title}]({prev_stem}.ipynb).\n"
            "- Concepts and notation introduced in the previous notebook."
        )
    cells.append(_md_cell(prereq_text))

    # --- Section + code cell pairs ---
    for heading, code in sections:
        cells.append(_md_cell(f"## {heading}"))
        cells.append(_code_cell(code))

    # --- Exercises section ---
    cells.append(_md_cell(
        "## Exercises\n"
        "\n"
        "Try these on your own before moving on:\n"
        "\n"
        "1. **Exercise 1:** *(TODO: add exercise)*\n"
        "2. **Exercise 2:** *(TODO: add exercise)*\n"
        "3. **Exercise 3:** *(TODO: add exercise)*"
    ))

    # --- Summary cell with Next link ---
    next_link = _next_notebook_link(module_path, notebooks, idx)
    cells.append(_md_cell(
        f"## Summary\n"
        f"\n"
        f"In this notebook we explored **{title.lower()}**.  "
        f"Key takeaways:\n"
        f"\n"
        f"- *(TODO: summarize key point 1)*\n"
        f"- *(TODO: summarize key point 2)*\n"
        f"- *(TODO: summarize key point 3)*"
        f"{next_link}"
    ))

    return {
        "cells": cells,
        "metadata": SAGEMATH_KERNEL,
        "nbformat": 4,
        "nbformat_minor": 5,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    total = 0

    for module_path, notebooks in MODULES.items():
        sage_dir = REPO_ROOT / module_path / "sage"
        sage_dir.mkdir(parents=True, exist_ok=True)

        for idx, (stem, title, description, sections) in enumerate(notebooks):
            nb = _build_notebook(
                module_path, notebooks, idx,
                stem, title, description, sections,
            )

            out_path = sage_dir / f"{stem}.ipynb"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=1, ensure_ascii=False)
                f.write("\n")

            rel = out_path.relative_to(REPO_ROOT)
            print(f"  created  {rel}")
            total += 1

    print(f"\nDone: {total} notebooks generated.")


if __name__ == "__main__":
    main()
