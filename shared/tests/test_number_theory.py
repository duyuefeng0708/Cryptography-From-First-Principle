"""Tests for cryptolab.number_theory."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cryptolab.number_theory import (
    gcd, extended_gcd, euler_phi, factor, divisors, is_prime,
    power_mod, inverse_mod, primitive_root, crt, discrete_log,
)
import pytest


# --- gcd ---

def test_gcd_basic():
    assert gcd(12, 8) == 4
    assert gcd(17, 13) == 1
    assert gcd(0, 5) == 5
    assert gcd(5, 0) == 5
    assert gcd(0, 0) == 0

def test_gcd_negative():
    assert gcd(-12, 8) == 4
    assert gcd(12, -8) == 4


# --- extended_gcd ---

def test_extended_gcd():
    g, s, t = extended_gcd(35, 15)
    assert g == 5
    assert 35 * s + 15 * t == g

def test_extended_gcd_coprime():
    g, s, t = extended_gcd(7, 11)
    assert g == 1
    assert 7 * s + 11 * t == 1


# --- factor ---

def test_factor():
    assert factor(60) == {2: 2, 3: 1, 5: 1}
    assert factor(1) == {}
    assert factor(17) == {17: 1}
    assert factor(2**10) == {2: 10}

def test_factor_zero():
    assert factor(0) == {}


# --- divisors ---

def test_divisors():
    assert divisors(12) == [1, 2, 3, 4, 6, 12]
    assert divisors(1) == [1]
    assert divisors(17) == [1, 17]
    assert divisors(0) == []


# --- is_prime ---

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(17) is True
    assert is_prime(1) is False
    assert is_prime(0) is False
    assert is_prime(97) is True
    assert is_prime(100) is False


# --- euler_phi ---

def test_euler_phi():
    assert euler_phi(1) == 1
    assert euler_phi(7) == 6
    assert euler_phi(12) == 4
    assert euler_phi(30) == 8
    # phi(p) = p - 1 for prime p
    assert euler_phi(97) == 96


# --- power_mod ---

def test_power_mod():
    assert power_mod(2, 10, 1000) == 1024 % 1000
    assert power_mod(3, 0, 7) == 1
    assert power_mod(5, 1, 13) == 5
    assert power_mod(2, 10, 1) == 0

def test_power_mod_negative_exp():
    # 3^(-1) mod 7 = 5 (since 3*5 = 15 = 1 mod 7)
    assert power_mod(3, -1, 7) == 5


# --- inverse_mod ---

def test_inverse_mod():
    assert inverse_mod(3, 7) == 5  # 3*5 = 15 = 1 mod 7
    assert inverse_mod(2, 11) == 6  # 2*6 = 12 = 1 mod 11

def test_inverse_mod_no_inverse():
    with pytest.raises(ValueError):
        inverse_mod(2, 4)


# --- primitive_root ---

def test_primitive_root():
    g = primitive_root(7)
    assert g == 3  # 3 is the smallest primitive root mod 7
    # Verify it has order 6
    assert power_mod(g, 6, 7) == 1
    for k in range(1, 6):
        assert power_mod(g, k, 7) != 1

def test_primitive_root_small():
    assert primitive_root(2) == 1
    assert primitive_root(5) == 2


# --- crt ---

def test_crt():
    # x = 2 mod 3, x = 3 mod 5 -> x = 8 mod 15
    assert crt([2, 3], [3, 5]) == 8

def test_crt_three_moduli():
    # x = 1 mod 2, x = 2 mod 3, x = 3 mod 5 -> x = 23 mod 30
    assert crt([1, 2, 3], [2, 3, 5]) == 23


# --- discrete_log ---

def test_discrete_log():
    # 3^x = 6 mod 7
    # 3^1=3, 3^2=2, 3^3=6 -> x=3
    assert discrete_log(6, 3, 7) == 3

def test_discrete_log_identity():
    # g^0 = 1
    assert discrete_log(1, 3, 7) == 0
