# Module 07: Bilinear Pairings

A map between curve groups that unlocks BLS signatures, IBE, and the road to SNARKs.

## Prerequisites

- [Module 06: Elliptic Curves](../../foundations/06-elliptic-curves/) — scalar multiplication, curve groups, and the elliptic-curve discrete-log setting

## Learning Objectives

After completing this module you will:
1. Understand the definition and key properties of a bilinear map
2. Build geometric intuition for the Weil pairing on elliptic curves
3. Implement the BLS signature scheme (sign, verify, aggregate)
4. Grasp how pairings enable identity-based encryption (IBE)

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Bilinear Maps: Definition](sage/07a-bilinear-maps-definition.ipynb) | What a bilinear map is and why bilinearity + non-degeneracy matter |
| b | [Weil Pairing Intuition](sage/07b-weil-pairing-intuition.ipynb) | Geometric picture of the Weil pairing via divisors on curves |
| c | [Pairing-Friendly Curves](sage/07c-pairing-friendly-curves.ipynb) | Why only certain curves admit efficient pairings, embedding degree |
| d | [BLS Signatures](sage/07d-bls-signatures.ipynb) | Sign, verify, and aggregate signatures using a single pairing check |
| e | [Identity-Based Encryption](sage/07e-identity-based-encryption.ipynb) | Encrypt to an identity string instead of a public key |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `bls_sign` | Sign a message using a private scalar and hash-to-curve |
| 2 | `bls_verify` | Verify a BLS signature via a pairing equation check |
| 3 | `bls_aggregate_sigs` | Aggregate multiple BLS signatures into one curve point |
| 4 | `bls_aggregate_verify` | Verify an aggregate signature against multiple public keys |

Run: `cargo test -p pairings`

## Break

Attack exercises in `break/`:
- **Rogue key attack on naive BLS aggregation** — craft a malicious public key that lets you forge an aggregate signature without knowing all private keys
- **Pairing inversion attempt** — try to recover discrete logs from pairing outputs and see why the pairing-inversion problem is hard

## Connect

Real-world appearances in `connect/`:
- **BLS signatures in Ethereum 2.0 consensus** — validators sign attestations with BLS; aggregation keeps beacon-chain overhead manageable
- **Pairing-based identity-based encryption** — Boneh-Franklin IBE lets any string serve as a public key, used in enterprise key management

---
*Next: [Module 08: Lattices and Post-Quantum Cryptography](../08-lattices-post-quantum/)*
