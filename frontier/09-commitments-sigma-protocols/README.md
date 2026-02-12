# Module 09: Commitment Schemes and Sigma Protocols

[![View on nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/duyuefeng0708/Cryptography-From-First-Principle/tree/main/frontier/09-commitments-sigma-protocols/sage/)

How to prove you know a secret without revealing it. This is the foundation of zero knowledge.

## Prerequisites

- [Module 01: Modular Arithmetic](../../foundations/01-modular-arithmetic-groups/) (groups, generators, and the discrete log setting)
- [Module 06: Elliptic Curves](../../foundations/06-elliptic-curves/) (optional but helpful for Pedersen commitments over curves)

## Learning Objectives

After completing this module you will:
1. Understand the hiding and binding properties of commitment schemes
2. Implement Pedersen commitments and verify their homomorphic property
3. Grasp the three move sigma protocol structure (commit, challenge, response)
4. Implement the Schnorr identification protocol and the Fiat-Shamir transform to make it non-interactive

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Commitment Schemes](sage/09a-commitment-schemes.ipynb) | What "commit then reveal" means, hiding vs binding tradeoffs |
| b | [Pedersen Commitments](sage/09b-pedersen-commitments.ipynb) | Building perfectly hiding commitments from discrete log, homomorphic addition |
| c | [Sigma Protocols: Intuition](sage/09c-sigma-protocols-intuition.ipynb) | The three move pattern and why it achieves zero knowledge |
| d | [Schnorr Protocol](sage/09d-schnorr-protocol.ipynb) | Interactive proof of knowledge of a discrete log |
| e | [Fiat-Shamir Transform](sage/09e-fiat-shamir-transform.ipynb) | Replacing the verifier with a hash to get non-interactive proofs |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `pedersen_commit` | Commit to a value with a blinding factor using two generators |
| 2 | `pedersen_verify` | Verify that a commitment opens to the claimed value and blinding factor |
| 3 | `schnorr_prove` | Generate a Schnorr proof of knowledge of a discrete log |
| 4 | `schnorr_verify` | Verify a Schnorr proof against a public key |
| 5 | `fiat_shamir` | Derive a non-interactive challenge by hashing the transcript |

Run: `cargo test -p commitments-sigma`

## Break

Try these attacks in the `break/` folder:
- **Break Schnorr with bad randomness (nonce reuse).** Extract the secret key when the prover reuses a nonce across two protocol runs.
- **Forge commitment with wrong binding.** Demonstrate that a computationally unbounded adversary can open a Pedersen commitment two ways.

## Connect

See where this shows up in practice (in the `connect/` folder):
- **Schnorr signatures in Bitcoin Taproot.** BIP 340 uses Schnorr signatures for simpler multisig and privacy preserving script spending.
- **Commitments as building blocks for ZK proofs.** Pedersen commitments appear inside Bulletproofs, Groth16 inputs, and polynomial commitment schemes.

---
*Next: [Module 10: SNARKs and STARKs](../10-snarks-starks/)*
