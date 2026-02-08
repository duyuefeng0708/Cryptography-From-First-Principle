# Crypto From First Principles

Open-source cryptography teaching materials for BSc and postgraduate students.
Learn the math, build it in Rust, break it, then see it in the wild.

## Philosophy

Traditional crypto education either drowns you in pure math or hands you a library.
We bridge the gap: **algebra → intuition → working code → real protocols**.

Every module follows four phases:

1. **Explore** (SageMath) — Interactive notebooks to build mathematical intuition
2. **Implement** (Rust) — Build the cryptographic primitive from scratch
3. **Break** — Attack weakened versions to understand why parameters matter
4. **Connect** — Trace the math to real protocols (TLS, Signal, Zcash...)

## Structure

### Part I — Foundations (BSc)

| # | Module | Key Concepts |
|---|--------|-------------|
| 01 | Modular Arithmetic & Groups | Cyclic groups, generators, order, Lagrange's theorem |
| 02 | Rings, Fields & Polynomials | Ring axioms, ideals, polynomial rings, irreducibility |
| 03 | Galois Fields & AES | GF(2^n), AES S-box, MixColumns as field arithmetic |
| 04 | Number Theory & RSA | Euler/Fermat, CRT, RSA internals, padding |
| 05 | Discrete Log & Diffie-Hellman | DLP, CDH, DDH, key exchange |
| 06 | Elliptic Curves | Weierstrass form, point addition, ECDH, ECDSA |

### Part II — Frontier (Postgraduate)

| # | Module | Key Concepts |
|---|--------|-------------|
| 07 | Bilinear Pairings | Weil/Tate pairing, BLS signatures, IBE |
| 08 | Lattices & Post-Quantum | LWE, Ring-LWE, NTRU, Kyber/Dilithium |
| 09 | Commitments & Sigma Protocols | Pedersen, Schnorr, Fiat-Shamir |
| 10 | SNARKs & STARKs | R1CS, QAP, Groth16, FRI |
| 11 | Homomorphic Encryption | BGV, BFV, CKKS |
| 12 | Multi-Party Computation | Secret sharing, Yao's GC, SPDZ |

## Prerequisites

- **SageMath** ≥ 10.0 — [Install](https://www.sagemath.org/download.html)
- **Rust** ≥ 1.75 — [Install](https://rustup.rs)
- **Jupyter** with SageMath kernel

## License

MIT
