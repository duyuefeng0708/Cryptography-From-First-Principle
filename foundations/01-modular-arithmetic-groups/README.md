# Module 01: Modular Arithmetic and Groups

From clock arithmetic to the algebraic structures that underpin all of cryptography.

## Prerequisites

No prior modules needed. This is the starting point.

## Learning Objectives

After completing this module you will:
1. Understand modular arithmetic as a system, not just a calculation trick
2. Recognize group structure in Z_n and Z_n*
3. Compute generators and orders of cyclic groups
4. Apply Lagrange's theorem to reason about subgroup structure

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Integers and Division](sage/01a-integers-and-division.ipynb) | Divisibility, remainders, and the division algorithm |
| b | [Modular Arithmetic](sage/01b-modular-arithmetic.ipynb) | Addition, multiplication, and exponentiation mod n |
| c | [Groups: First Look](sage/01c-groups-first-look.ipynb) | What makes a set + operation a group |
| d | [Cyclic Groups and Generators](sage/01d-cyclic-groups-generators.ipynb) | Generators, cyclic structure, and element orders |
| e | [Subgroups and Lagrange](sage/01e-subgroups-lagrange.ipynb) | Subgroups, cosets, and Lagrange's theorem |
| f | [Group Visualization](sage/01f-group-visualization.ipynb) | Cayley tables, cycle graphs, and visual intuition |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `mod_exp` | Modular exponentiation via repeated squaring |
| 2 | `gcd` | Greatest common divisor (Euclidean algorithm) |
| 3 | `is_generator` | Test whether an element generates the full group |
| 4 | `element_order` | Compute the multiplicative order of an element |
| 5 | `find_all_generators` | Enumerate every generator of Z_n* |

Run: `cargo test -p mod-arith-groups`

## Break

Try these attacks in the `break/` folder:
- Recover a secret from a group with smooth order by factoring the order and solving in each subgroup
- Exploit weak generator choice to reduce the search space of a brute force attack

## Connect

See where this shows up in practice (in the `connect/` folder):
- RSA key generation relies on modular arithmetic for encryption and decryption
- Diffie-Hellman parameter selection: choosing a safe prime ensures the group has strong structure

---
*Next: [Module 02: Rings, Fields, and Polynomials](../02-rings-fields-polynomials/)*
