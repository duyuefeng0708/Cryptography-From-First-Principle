# Module 02: Rings, Fields, and Polynomials

Adding a second operation opens the door to polynomial algebra and field extensions.

## Prerequisites

- [Module 01: Modular Arithmetic and Groups](../01-modular-arithmetic-groups/) (groups, modular arithmetic)

## Learning Objectives

After completing this module you will:
1. Distinguish rings from groups and fields by their algebraic properties
2. Work with polynomial rings over finite fields
3. Test polynomials for irreducibility over a given field
4. Construct quotient rings and understand their role in building new algebraic structures

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [What Is a Ring?](sage/02a-what-is-a-ring.ipynb) | Ring axioms, examples, and non-examples |
| b | [Integers mod n as a Ring](sage/02b-integers-mod-n-as-ring.ipynb) | Z_n with both addition and multiplication |
| c | [Polynomial Rings](sage/02c-polynomial-rings.ipynb) | Building and manipulating polynomials over finite fields |
| d | [What Is a Field?](sage/02d-what-is-a-field.ipynb) | Fields as rings where every nonzero element has an inverse |
| e | [Polynomial Division and Irreducibility](sage/02e-polynomial-division-irreducibility.ipynb) | Long division, remainders, and irreducibility tests |
| f | [Quotient Rings](sage/02f-quotient-rings.ipynb) | Modding out by an ideal to create new structures |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `poly_eval` | Evaluate a polynomial at a given point over a finite field |
| 2 | `poly_add` | Add two polynomials coefficient-wise with reduction |
| 3 | `poly_mul` | Multiply two polynomials with coefficient reduction |
| 4 | `poly_div_rem` | Polynomial long division returning quotient and remainder |
| 5 | `is_irreducible_mod_p` | Test whether a polynomial is irreducible over F_p |

Run: `cargo test -p rings-fields-poly`

## Break

Try these attacks in the `break/` folder:
- Factor a "supposedly irreducible" polynomial to break a scheme built on a quotient ring
- Find zero divisors in Z_n for composite n and show why Z_n fails to be a field

## Connect

See where this shows up in practice (in the `connect/` folder):
- AES uses GF(2^8), where all field arithmetic lives in a polynomial quotient ring
- Reed-Solomon error correcting codes rely on polynomial evaluation and interpolation over finite fields

---
*Next: [Module 03: Galois Fields and AES](../03-galois-fields-aes/)*
