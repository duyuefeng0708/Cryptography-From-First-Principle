# Module 12: Multi-Party Computation

Multiple parties compute a joint function without revealing their private inputs.

## Prerequisites

- [Module 01: Modular Arithmetic](../../foundations/01-modular-arithmetic/) — modular arithmetic and polynomial evaluation over finite fields
- [Module 09: Commitment Schemes and Sigma Protocols](../09-commitments-sigma-protocols/) — commitments, helpful for achieving malicious security

## Learning Objectives

After completing this module you will:
1. Implement Shamir and additive secret sharing and understand their threshold properties
2. Understand Yao's garbled circuits for secure two-party computation
3. Grasp oblivious transfer and its role as an MPC building block
4. See how the SPDZ protocol achieves malicious security using MACs and preprocessing

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Secret Sharing: Shamir](sage/12a-secret-sharing-shamir.ipynb) | Splitting a secret into polynomial shares with a (t, n) threshold |
| b | [Secret Sharing: Additive](sage/12b-secret-sharing-additive.ipynb) | The simplest sharing scheme — random splits that sum to the secret |
| c | [Yao's Garbled Circuits](sage/12c-yaos-garbled-circuits.ipynb) | Encrypting a Boolean circuit so one party evaluates without learning inputs |
| d | [Oblivious Transfer](sage/12d-oblivious-transfer.ipynb) | A sender offers two messages; the receiver learns exactly one, sender learns nothing |
| e | [SPDZ Protocol](sage/12e-spdz-protocol.ipynb) | Preprocessing Beaver triples and MAC-based verification for malicious security |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `shamir_share` | Split a secret into n shares using a random degree-(t-1) polynomial |
| 2 | `shamir_reconstruct` | Reconstruct the secret from t or more shares via Lagrange interpolation |
| 3 | `additive_share` | Split a secret into n additive shares over a finite field |
| 4 | `additive_reconstruct` | Reconstruct the secret by summing all additive shares |
| 5 | `beaver_triple_mul` | Perform a secret-shared multiplication using a preprocessed Beaver triple |

Run: `cargo test -p mpc`

## Break

Attack exercises in `break/`:
- **Cheating dealer detection in Shamir sharing** — detect when a dealer distributes inconsistent shares by using verification polynomials
- **Corrupt party in additive sharing** — observe how a single malicious party can bias the output and why MACs are needed

## Connect

Real-world appearances in `connect/`:
- **Threshold wallets in cryptocurrency** — split a signing key across multiple devices or custodians so no single point of compromise exists
- **Private set intersection** — two parties discover shared contacts without revealing their full lists (used in contact tracing and ad measurement)
- **Secure auctions** — compute the winning bid without revealing any losing bids to the auctioneer

---
*This is the final module in the series.*
