"""Tests for cryptolab.modular."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cryptolab.modular import Mod, Zmod, ZmodRing
import pytest


# --- Mod basics ---

def test_mod_creation():
    a = Mod(10, 7)
    assert int(a) == 3
    assert a.modulus == 7

def test_mod_repr():
    a = Mod(3, 7)
    assert repr(a) == '3'
    assert str(a) == '3'

def test_mod_negative_value():
    a = Mod(-1, 7)
    assert int(a) == 6


# --- Mod arithmetic ---

def test_mod_add():
    assert Mod(3, 7) + Mod(5, 7) == Mod(1, 7)

def test_mod_sub():
    assert Mod(2, 7) - Mod(5, 7) == Mod(4, 7)

def test_mod_mul():
    assert Mod(3, 7) * Mod(4, 7) == Mod(5, 7)

def test_mod_pow():
    assert Mod(3, 7) ** 2 == Mod(2, 7)

def test_mod_neg():
    assert -Mod(3, 7) == Mod(4, 7)

def test_mod_invert():
    assert ~Mod(3, 7) == Mod(5, 7)
    # Verify: 3 * 5 = 15 = 1 mod 7
    assert Mod(3, 7) * ~Mod(3, 7) == Mod(1, 7)

def test_mod_pow_negative():
    # 3^(-1) mod 7 = 5
    assert Mod(3, 7) ** (-1) == Mod(5, 7)

def test_mod_div():
    # 6 / 3 mod 7 = 6 * 5 = 30 = 2 mod 7
    assert Mod(6, 7) / Mod(3, 7) == Mod(2, 7)


# --- Mod with int ---

def test_mod_add_int():
    assert Mod(3, 7) + 5 == Mod(1, 7)
    assert 5 + Mod(3, 7) == Mod(1, 7)

def test_mod_mul_int():
    assert Mod(3, 7) * 4 == Mod(5, 7)
    assert 4 * Mod(3, 7) == Mod(5, 7)


# --- Mod incompatible ---

def test_mod_different_modulus():
    with pytest.raises(ValueError):
        Mod(3, 7) + Mod(3, 5)


# --- Mod comparison and hashing ---

def test_mod_eq():
    assert Mod(3, 7) == Mod(3, 7)
    assert Mod(3, 7) == Mod(10, 7)
    assert Mod(3, 7) != Mod(4, 7)

def test_mod_hash():
    s = {Mod(3, 7), Mod(10, 7), Mod(4, 7)}
    assert len(s) == 2  # 3 and 10 are the same mod 7

def test_mod_eq_int():
    assert Mod(3, 7) == 3
    assert Mod(3, 7) == 10  # 10 % 7 = 3


# --- Mod group theory ---

def test_multiplicative_order():
    # ord(3) in (Z/7Z)* = 6 (3 is a primitive root mod 7)
    assert Mod(3, 7).multiplicative_order() == 6
    # ord(2) in (Z/7Z)* = 3 (2^3 = 8 = 1 mod 7)
    assert Mod(2, 7).multiplicative_order() == 3

def test_additive_order():
    # additive order of 4 in Z/12Z = 12/gcd(4,12) = 12/4 = 3
    assert Mod(4, 12).additive_order() == 3
    assert Mod(1, 12).additive_order() == 12
    assert Mod(0, 12).additive_order() == 1

def test_multiplicative_order_non_unit():
    with pytest.raises(ValueError):
        Mod(2, 4).multiplicative_order()


# --- ZmodRing ---

def test_zmod_creation():
    R = Zmod(7)
    assert R.order() == 7

def test_zmod_call():
    R = Zmod(7)
    a = R(10)
    assert int(a) == 3

def test_zmod_iter():
    R = Zmod(5)
    elts = list(R)
    assert len(elts) == 5
    assert [int(x) for x in elts] == [0, 1, 2, 3, 4]

def test_zmod_list():
    R = Zmod(4)
    assert len(R.list()) == 4

def test_zmod_multiplicative_group():
    R = Zmod(12)
    units = R.list_of_elements_of_multiplicative_group()
    assert [int(u) for u in units] == [1, 5, 7, 11]

def test_zmod_contains():
    R = Zmod(7)
    assert Mod(3, 7) in R
    assert Mod(3, 5) not in R


# --- Operation tables ---

def test_addition_table_list():
    R = Zmod(3)
    table = R.addition_table(style='list')
    # Row 0: [0+0, 0+1, 0+2] = [0, 1, 2]
    assert table[0] == [0, 1, 2]
    # Row 1: [1+0, 1+1, 1+2] = [1, 2, 0]
    assert table[1] == [1, 2, 0]

def test_multiplication_table_list():
    R = Zmod(4)
    table = R.multiplication_table(style='list')
    # Row 2: [2*0, 2*1, 2*2, 2*3] = [0, 2, 0, 2]
    assert table[2] == [0, 2, 0, 2]
