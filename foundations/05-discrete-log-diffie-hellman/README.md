# Module 05: The Discrete Logarithm and Diffie-Hellman

The hardness assumption that powers key exchange and much of modern crypto.

## Prerequisites

- [Module 01: Modular Arithmetic and Groups](../01-modular-arithmetic-groups/) (cyclic groups, generators)
- [Module 04: Number Theory and RSA](../04-number-theory-rsa/) (number theory basics)

## Learning Objectives

After completing this module you will:
1. Understand the discrete logarithm problem and why it is believed to be hard
2. Implement Diffie-Hellman key exchange from scratch
3. Analyze the CDH and DDH hardness assumptions and their relationships
4. Apply baby step giant step and Pohlig-Hellman algorithms to solve discrete logs in weak groups

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [The Discrete Log Problem](sage/05a-the-discrete-log-problem.ipynb) | What the DLP is and why brute force fails for large groups |
| b | [Primitive Roots and Generators](sage/05b-primitive-roots-generators.ipynb) | Finding and verifying generators of Z_p* |
| c | [Diffie-Hellman Key Exchange](sage/05c-diffie-hellman-key-exchange.ipynb) | The protocol, step by step, with concrete examples |
| d | [Computational Hardness: CDH and DDH](sage/05d-computational-hardness-cdh-ddh.ipynb) | CDH, DDH, and the hierarchy of assumptions |
| e | [Baby Step Giant Step](sage/05e-baby-step-giant-step.ipynb) | A time/space tradeoff that solves DLP in O(sqrt(n)) |
| f | [Pohlig-Hellman](sage/05f-pohlig-hellman.ipynb) | Exploiting smooth group orders to decompose the DLP |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `discrete_log_brute` | Brute force discrete log for small groups |
| 2 | `baby_step_giant_step` | Baby step giant step algorithm |
| 3 | `diffie_hellman` | Compute a Diffie-Hellman shared secret |
| 4 | `pohlig_hellman` | Pohlig-Hellman algorithm for smooth order groups |
| 5 | `is_safe_prime` | Test whether a prime p is safe (p = 2q + 1 with q prime) |

Run: `cargo test -p dlog-dh`

## Break

Try these attacks in the `break/` folder:
- Small subgroup attack on DH with an unsafe prime, forcing the shared secret into a small subgroup
- Pohlig-Hellman on a smooth order group, recovering the secret exponent by solving small DLPs
- Recover a shared secret from leaked partial bits using lattice or meet in the middle techniques

## Connect

See where this shows up in practice (in the `connect/` folder):
- Diffie-Hellman in TLS 1.3 key exchange, where the ephemeral DH handshake establishes session keys
- DH in the Signal protocol (X3DH), where the extended triple Diffie-Hellman protocol bootstraps end to end encryption

---
*Next: [Module 06: Elliptic Curves](../06-elliptic-curves/)*
