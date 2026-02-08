# Module 04: Number Theory and RSA

The number theory that makes RSA work, and the attacks that break it when the math is sloppy.

## Prerequisites

- [Module 01: Modular Arithmetic and Groups](../01-modular-arithmetic-groups/) (modular arithmetic, groups)

## Learning Objectives

After completing this module you will:
1. Implement the extended Euclidean algorithm and use it to compute modular inverses
2. Apply Euler's theorem and the Chinese Remainder Theorem
3. Generate RSA keys from first principles (prime selection, key pair computation)
4. Understand textbook RSA's limitations and why padding is essential

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Divisibility, GCD, and Euclid](sage/04a-divisibility-gcd-euclid.ipynb) | The Euclidean algorithm and its correctness |
| b | [Extended Euclidean Algorithm](sage/04b-extended-euclidean-algorithm.ipynb) | Computing Bezout coefficients and modular inverses |
| c | [Euler's Totient and Fermat's Theorem](sage/04c-euler-totient-fermats-theorem.ipynb) | Why a^phi(n) = 1 mod n and how RSA uses this |
| d | [Chinese Remainder Theorem](sage/04d-chinese-remainder-theorem.ipynb) | Solving simultaneous congruences and CRT based RSA speedup |
| e | [RSA Key Generation](sage/04e-rsa-key-generation.ipynb) | Choosing primes, computing e and d, the full key generation process |
| f | [RSA Encryption and Decryption](sage/04f-rsa-encryption-decryption.ipynb) | Textbook RSA in action and its pitfalls |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `extended_gcd` | Extended Euclidean algorithm returning (gcd, x, y) |
| 2 | `mod_inverse` | Modular multiplicative inverse via extended GCD |
| 3 | `euler_totient` | Compute Euler's totient function for a given n |
| 4 | `rsa_keygen` | Generate an RSA key pair (n, e, d) from two primes |
| 5 | `rsa_encrypt_decrypt` | Textbook RSA encryption and decryption |

Run: `cargo test -p number-theory-rsa`

## Break

Try these attacks in the `break/` folder:
- Hastad's broadcast attack: recover plaintext from multiple ciphertexts when e is small and no padding is used
- Wiener's attack on small d: exploit a small private exponent via continued fractions
- Factor N when |p - q| is small using Fermat's factorization method

## Connect

See where this shows up in practice (in the `connect/` folder):
- RSA in TLS certificates and PKCS#1, where RSA signs the certificates that authenticate web servers
- RSA-OAEP padding in practice, showing why textbook RSA is never used and how OAEP fixes it

---
*Next: [Module 05: The Discrete Logarithm and Diffie-Hellman](../05-discrete-log-diffie-hellman/)*
