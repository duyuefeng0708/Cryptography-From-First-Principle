# Module 08: Lattices and Post-Quantum Cryptography

The geometry of integer grids — and why quantum computers can't break them.

## Prerequisites

- [Module 01: Modular Arithmetic](../../foundations/01-modular-arithmetic/) — modular reduction, congruences, and arithmetic in Z_n
- Linear algebra familiarity (bases, linear independence, inner products)

## Learning Objectives

After completing this module you will:
1. Understand lattice bases, the shortest vector problem (SVP), and the closest vector problem (CVP)
2. Apply the LLL algorithm to reduce a lattice basis and break weak schemes
3. Grasp the Learning With Errors (LWE) and Ring-LWE hardness assumptions
4. See how Kyber/ML-KEM works at a high level and why it resists quantum attack

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Lattices and Bases](sage/08a-lattices-and-bases.ipynb) | What a lattice is, how different bases span the same lattice, visualizing in 2D |
| b | [Shortest Vector Problem](sage/08b-shortest-vector-problem.ipynb) | Why finding short vectors is hard, and how SVP/CVP relate to cryptography |
| c | [LLL Algorithm](sage/08c-lll-algorithm.ipynb) | Step-by-step LLL basis reduction with animated lattice plots |
| d | [Learning With Errors](sage/08d-learning-with-errors.ipynb) | The LWE problem: hiding secrets in noisy linear equations |
| e | [Ring-LWE](sage/08e-ring-lwe.ipynb) | Adding polynomial ring structure for efficiency |
| f | [Kyber Overview](sage/08f-kyber-overview.ipynb) | End-to-end walkthrough of ML-KEM key encapsulation |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `gram_schmidt_2d` | Compute the Gram-Schmidt orthogonalization of a 2D lattice basis |
| 2 | `lll_reduce_2d` | Run LLL basis reduction on a 2D lattice |
| 3 | `lwe_keygen` | Generate an LWE public/private key pair with error sampling |
| 4 | `lwe_encrypt` | Encrypt a single bit under an LWE public key |
| 5 | `lwe_decrypt` | Decrypt an LWE ciphertext using the secret key |

Run: `cargo test -p lattices-pq`

## Break

Attack exercises in `break/`:
- **LLL attack on a low-dimension lattice scheme** — use basis reduction to recover the secret key when the lattice dimension is too small
- **Recover LWE secret with no noise** — observe how removing the error term makes LWE trivially solvable via Gaussian elimination

## Connect

Real-world appearances in `connect/`:
- **NIST PQC standards** — ML-KEM (Kyber) for key encapsulation and ML-DSA (Dilithium) for digital signatures are the first post-quantum standards
- **Hybrid TLS with post-quantum** — Chrome and Cloudflare already deploy X25519+ML-KEM hybrid key exchange to hedge against quantum threats

---
*Next: [Module 09: Commitment Schemes and Sigma Protocols](../09-commitments-sigma-protocols/)*
