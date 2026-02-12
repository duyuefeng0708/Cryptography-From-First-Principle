# Module 06: Elliptic Curves

[![View on nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/duyuefeng0708/Cryptography-From-First-Principle/tree/main/foundations/06-elliptic-curves/sage/)

The same group theory, a different (and better) group. These curves power modern crypto.

## Prerequisites

- [Module 01: Modular Arithmetic and Groups](../01-modular-arithmetic-groups/) (groups)
- [Module 02: Rings, Fields, and Polynomials](../02-rings-fields-polynomials/) (fields)
- [Module 05: The Discrete Logarithm and Diffie-Hellman](../05-discrete-log-diffie-hellman/) (DLP, Diffie-Hellman)

## Learning Objectives

After completing this module you will:
1. Understand the elliptic curve group law geometrically (over the reals) and algebraically (over finite fields)
2. Implement point addition and scalar multiplication from scratch
3. Apply ECDH for key exchange and ECDSA for digital signatures
4. See why the EC discrete log problem is harder than the DLP in Z_p*, enabling shorter keys

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Curves over the Reals](sage/06a-curves-over-reals.ipynb) | The geometry of elliptic curves and the chord and tangent rule |
| b | [Point Addition Geometry](sage/06b-point-addition-geometry.ipynb) | Visualizing the group operation step by step |
| c | [Curves over Finite Fields](sage/06c-curves-over-finite-fields.ipynb) | Moving from continuous curves to discrete point sets |
| d | [Group Structure and Order](sage/06d-group-structure-and-order.ipynb) | Hasse's theorem, point counting, and group structure |
| e | [Scalar Multiplication](sage/06e-scalar-multiplication.ipynb) | Double and add algorithm for efficient scalar multiplication |
| f | [ECDH and ECDSA](sage/06f-ecdh-and-ecdsa.ipynb) | Key exchange and signatures on elliptic curves |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `point_add` | Add two points on an elliptic curve over a prime field |
| 2 | `point_double` | Double a point (tangent line case of the group law) |
| 3 | `scalar_mul` | Scalar multiplication via double and add |
| 4 | `ecdh_shared_secret` | Compute an ECDH shared secret from a private key and public point |
| 5 | `ecdsa_verify` | Verify an ECDSA signature given a message, signature, and public key |

Run: `cargo test -p elliptic-curves`

## Break

Try these attacks in the `break/` folder:
- ECDSA nonce reuse (the PlayStation 3 hack): recover the private key when the same nonce is used twice
- Invalid curve attack: send a point not on the curve to extract bits of the secret
- Small subgroup on the twist: exploit points on the quadratic twist to leak secret key information

## Connect

See where this shows up in practice (in the `connect/` folder):
- ECDH (X25519) in TLS 1.3 is the default key exchange in modern HTTPS connections
- ECDSA in Bitcoin/Ethereum, where every transaction is authorized by an ECDSA signature on secp256k1
- Ed25519 in SSH is the recommended signing algorithm for SSH keys

---
*Next: [Module 07: Pairings](../../frontier/07-pairings/)*
