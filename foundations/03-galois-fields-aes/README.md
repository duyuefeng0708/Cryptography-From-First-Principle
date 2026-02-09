# Module 03: Galois Fields and AES

[![View on nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/duyuefeng0708/learn-cryptography/tree/main/foundations/03-galois-fields-aes/sage/)

See how abstract field theory becomes the concrete engine inside AES.

## Prerequisites

- [Module 02: Rings, Fields, and Polynomials](../02-rings-fields-polynomials/) (fields, polynomial rings, quotient rings)

## Learning Objectives

After completing this module you will:
1. Construct GF(2^8) as a polynomial quotient ring
2. Perform field arithmetic (add, multiply, invert) in GF(256)
3. Understand every AES operation as a field theoretic transformation
4. Build the AES S-box from first principles using field inverses and affine maps

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Binary Fields: GF(2)](sage/03a-binary-fields-gf2.ipynb) | The simplest field and why it matters for computing |
| b | [Extension Fields: GF(2^n)](sage/03b-extension-fields-gf2n.ipynb) | Building larger fields from GF(2) using irreducible polynomials |
| c | [GF(256) Arithmetic](sage/03c-gf256-arithmetic.ipynb) | Addition as XOR, multiplication via polynomial reduction |
| d | [AES S-box Construction](sage/03d-aes-sbox-construction.ipynb) | Field inverse + affine transform = the S-box |
| e | [AES MixColumns as Field Ops](sage/03e-aes-mixcolumns-as-field-ops.ipynb) | MixColumns as matrix multiplication over GF(256) |
| f | [Full AES Round](sage/03f-full-aes-round.ipynb) | SubBytes, ShiftRows, MixColumns, AddRoundKey end to end |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `gf256_add` | Addition in GF(256) (XOR) |
| 2 | `gf256_mul` | Multiplication in GF(256) with reduction by the AES polynomial |
| 3 | `gf256_inv` | Multiplicative inverse in GF(256) |
| 4 | `aes_sbox` | Compute a single S-box output from the field inverse + affine map |
| 5 | `aes_mix_column` | Apply MixColumns to one column using GF(256) matrix multiplication |

Run: `cargo test -p galois-fields-aes`

## Break

Try these attacks in the `break/` folder:
- Construct a weak S-box using a reducible polynomial and show the resulting algebraic vulnerability
- Show why ECB mode leaks patterns by encrypting a structured image

## Connect

See where this shows up in practice (in the `connect/` folder):
- AES 128/256 in TLS 1.3 is the cipher suite that protects most web traffic
- AES-GCM authenticated encryption combines AES with Galois field based authentication

---
*Next: [Module 04: Number Theory and RSA](../04-number-theory-rsa/)*
