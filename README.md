# Crypto From First Principles

[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Open-source cryptography teaching materials for BSc and postgraduate students.
Learn the math, build it in Rust, break it, then see it in the wild.

## Quick Start

```bash
git clone https://github.com/YOUR-USER/crypto-from-first-principles.git
cd crypto-from-first-principles
conda activate sage
jupyter notebook foundations/01-modular-arithmetic-groups/sage/01a-integers-and-division.ipynb
```

## Philosophy

Traditional crypto education either drowns you in pure math or hands you a library.
We bridge the gap: **algebra → intuition → working code → real protocols**.

Every module follows four phases:

1. **Explore** in SageMath notebooks that build mathematical intuition
2. **Implement** in Rust, building each cryptographic primitive from scratch
3. **Break** weakened versions to understand why parameters matter
4. **Connect** the math to real protocols like TLS, Signal, and Zcash

## Structure

### Foundations (BSc)

| # | Module | Key Concepts |
|---|--------|-------------|
| 01 | Modular Arithmetic & Groups | Cyclic groups, generators, order, Lagrange's theorem |
| 02 | Rings, Fields & Polynomials | Ring axioms, ideals, polynomial rings, irreducibility |
| 03 | Galois Fields & AES | GF(2^n), AES S-box, MixColumns as field arithmetic |
| 04 | Number Theory & RSA | Euler/Fermat, CRT, RSA internals, padding |
| 05 | Discrete Log & Diffie-Hellman | DLP, CDH, DDH, key exchange |
| 06 | Elliptic Curves | Weierstrass form, point addition, ECDH, ECDSA |

### Frontier (Postgraduate)

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
The `connect/` directory traces the math to real protocols. Find where your group theory shows up in TLS, where your elliptic curves appear in Signal, and so on.

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
# Rust: download and run the installer from https://rustup.rs

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

### VS Code Setup

Install the [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extension, then connect to a SageMath Jupyter server:

1. Start the server (inside the conda env):
   ```bash
   conda activate sage
   sage -n jupyter
   ```
2. Copy the URL with token from the terminal output (e.g. `http://localhost:8888/?token=abc123...`).
3. In VS Code, open any `.ipynb`, click **Select Kernel**, then **Existing Jupyter Server**, and paste the URL.
4. Select the **SageMath** kernel from the list.

The server stays running. You only need to do steps 2 through 4 once per session.

## Roadmap

- [x] SageMath exploration notebooks (72 notebooks across 12 modules)
- [x] Scaffolded Rust exercises (57 functions with progressive difficulty)
- [x] Module 01 break/connect notebooks (attack and protocol notebooks)
- [ ] Break/connect notebooks for Modules 02-12
- [ ] Binder integration for zero-install browser experience
- [ ] Community-contributed exercises and visualizations

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting issues, adding content, and submitting PRs.

## License

MIT
