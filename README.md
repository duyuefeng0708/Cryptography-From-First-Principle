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

## How to Work Through a Module

Each module has its own `README.md` with prerequisites, learning objectives, and a detailed roadmap. Here's the general workflow:

### 1. Explore (SageMath notebooks)
```bash
cd foundations/01-modular-arithmetic-groups/sage
jupyter notebook 01a-integers-and-division.ipynb
```
Work through the notebooks **in order** (a → b → c → ...). Each builds on the last with no logical jumps. Run every cell, modify examples, answer the exercises.

### 2. Implement (Rust exercises)
```bash
cd foundations/01-modular-arithmetic-groups/rust
cargo test -- --ignored test_mod_exp   # Run a specific exercise
cargo test -- --ignored               # Run all exercises in this module
```
Each `lib.rs` contains exercises ordered by difficulty. Replace `todo!()` with your implementation. Early modules provide loop skeletons and hints; later modules give only function signatures.

### 3. Break
Open the `break/` directory for guided attacks on weakened versions of the primitives you just built. These show *why* parameter choices and security properties matter.

### 4. Connect
The `connect/` directory traces the math to real-world protocols — find where your group theory shows up in TLS, where your elliptic curves appear in Signal, etc.

## Prerequisites

- **Rust** ≥ 1.75
- **SageMath** ≥ 10.0 (via conda)
- **Jupyter** with SageMath kernel

### Linux (Ubuntu/Debian)

```bash
# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# SageMath + Jupyter (via Miniforge)
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
bash Miniforge3-Linux-x86_64.sh
source ~/miniforge3/etc/profile.d/conda.sh
conda create -n sage sage jupyter -c conda-forge
conda activate sage

# Register SageMath kernel (visible to VS Code / JupyterLab outside the env)
python -m sage.repl.ipython_kernel.install --user

# Verify
rustc --version
jupyter kernelspec list   # should show "sagemath"
```

### macOS

```bash
# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# SageMath + Jupyter (via Miniforge)
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-$(uname -m).sh"
bash Miniforge3-MacOSX-$(uname -m).sh
source ~/miniforge3/etc/profile.d/conda.sh
conda create -n sage sage jupyter -c conda-forge
conda activate sage

# Register SageMath kernel
python -m sage.repl.ipython_kernel.install --user

# Verify
rustc --version
jupyter kernelspec list
```

### Windows

```powershell
# Rust — download and run the installer from https://rustup.rs

# SageMath + Jupyter (via Miniforge)
# Download Miniforge3-Windows-x86_64.exe from:
#   https://github.com/conda-forge/miniforge/releases/latest
# Run the installer, then open Miniforge Prompt:

conda create -n sage sage jupyter -c conda-forge
conda activate sage

# Register SageMath kernel
python -m sage.repl.ipython_kernel.install --user

# Verify
rustc --version
jupyter kernelspec list
```

> **VS Code users**: Install the [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extension. Open any `.ipynb`, click **Select Kernel** → **Jupyter Kernel** → **SageMath**.

## License

MIT
