# Module 11: Homomorphic Encryption

[![View on nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/duyuefeng0708/learn-cryptography/tree/main/frontier/11-homomorphic-encryption/sage/)

Computing on encrypted data, the holy grail of privacy preserving computation.

## Prerequisites

- [Module 08: Lattices and Post-Quantum Cryptography](../08-lattices-post-quantum/) (lattice foundations and LWE, the mathematical bedrock of FHE)

## Learning Objectives

After completing this module you will:
1. Understand the fully homomorphic encryption (FHE) concept and the role of noise budgets
2. Implement a partially homomorphic scheme (Paillier) supporting addition on ciphertexts
3. Grasp how BGV and BFV manage noise through modulus switching and relinearization
4. Understand CKKS approximate arithmetic for real number computation on encrypted data

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [What Is FHE?](sage/11a-what-is-fhe.ipynb) | The dream of computing on ciphertexts, noise growth, and bootstrapping |
| b | [Partially Homomorphic Schemes](sage/11b-partially-homomorphic-schemes.ipynb) | RSA (multiplicative) and Paillier (additive) as stepping stones to FHE |
| c | [BGV Scheme](sage/11c-bgv-scheme.ipynb) | Modulus switching to control noise in integer arithmetic |
| d | [BFV Scheme](sage/11d-bfv-scheme.ipynb) | Scale invariant variant of BGV with simpler noise management |
| e | [CKKS Approximate Arithmetic](sage/11e-ckks-approximate-arithmetic.ipynb) | Encoding real numbers and tolerating approximate decryption |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `paillier_keygen` | Generate a Paillier public/private key pair from two large primes |
| 2 | `paillier_encrypt` | Encrypt a plaintext integer under the Paillier public key |
| 3 | `paillier_add` | Homomorphically add two Paillier ciphertexts |
| 4 | `paillier_decrypt` | Decrypt a Paillier ciphertext using the private key |
| 5 | `paillier_scalar_mul` | Multiply a Paillier ciphertext by a plaintext scalar |

Run: `cargo test -p homomorphic-enc`

## Break

Try these attacks in the `break/` folder:
- **Exhaust noise budget in FHE.** Chain enough homomorphic multiplications to push noise past the decryption threshold and observe garbled output.
- **CPA attack on deterministic encryption.** Show that a homomorphic scheme without randomized encryption leaks plaintext equality.

## Connect

See where this shows up in practice (in the `connect/` folder):
- **FHE in privacy preserving machine learning.** Train or infer on encrypted medical/financial data without exposing it.
- **Encrypted databases.** Query encrypted records without the server ever seeing plaintext.
- **Microsoft SEAL and Google FHE compiler.** Production libraries making FHE accessible to application developers.

---
*Next: [Module 12: Multi-Party Computation](../12-mpc/)*
