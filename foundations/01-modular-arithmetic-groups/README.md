# Module 01: Modular Arithmetic and Groups

[![View on nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/duyuefeng0708/Cryptography-From-First-Principle/tree/main/foundations/01-modular-arithmetic-groups/sage/)

From clock arithmetic to the algebraic structures that underpin all of cryptography.

## Prerequisites

No prior modules needed. This is the starting point.

## Learning Objectives

After completing this module you will:
1. Understand modular arithmetic as a system, not just a calculation trick
2. Recognize group structure in Z_n and Z_n*
3. Compute generators and orders of cyclic groups
4. Apply Lagrange's theorem to reason about subgroup structure

## Two Ways to Run

Every notebook has two versions. Choose whichever works for you.

| | Python (browser) | SageMath |
|---|---|---|
| **Setup** | Zero install, runs in JupyterLite | Needs local install or Codespaces |
| **Launch time** | ~5 seconds | ~1 minute (Codespaces) or 10+ min (Binder) |
| **Best for** | Quick exploration, mobile, first-timers | Full algebra system, research-grade computations |

## Explore

Work through these notebooks in order:

| # | Notebook | Python | SageMath |
|---|----------|--------|----------|
| a | Integers and Division | [python](python/01a-integers-and-division.ipynb) | [sage](sage/01a-integers-and-division.ipynb) |
| b | Modular Arithmetic | [python](python/01b-modular-arithmetic.ipynb) | [sage](sage/01b-modular-arithmetic.ipynb) |
| c | Groups: First Look | [python](python/01c-groups-first-look.ipynb) | [sage](sage/01c-groups-first-look.ipynb) |
| d | Cyclic Groups and Generators | [python](python/01d-cyclic-groups-generators.ipynb) | [sage](sage/01d-cyclic-groups-generators.ipynb) |
| e | Subgroups and Lagrange | [python](python/01e-subgroups-lagrange.ipynb) | [sage](sage/01e-subgroups-lagrange.ipynb) |
| f | Group Visualization | [python](python/01f-group-visualization.ipynb) | [sage](sage/01f-group-visualization.ipynb) |

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

| Attack | Python | SageMath |
|--------|--------|----------|
| Smooth-Order Attack (Pohlig-Hellman) | [python](python/break-smooth-order-attack.ipynb) | [sage](sage/break-smooth-order-attack.ipynb) |
| Weak Generator Attack | [python](python/break-weak-generator-attack.ipynb) | [sage](sage/break-weak-generator-attack.ipynb) |

## Connect

| Application | Python | SageMath |
|-------------|--------|----------|
| RSA Key Generation | [python](python/connect-rsa-key-generation.ipynb) | [sage](sage/connect-rsa-key-generation.ipynb) |
| Diffie-Hellman Parameter Selection | [python](python/connect-dh-parameter-selection.ipynb) | [sage](sage/connect-dh-parameter-selection.ipynb) |

---
*Next: [Module 02: Rings, Fields, and Polynomials](../02-rings-fields-polynomials/)*
