# Ship to GitHub Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the repo GitHub-ready: CI, badges, community files, README polish, Rust cleanup, and break/connect notebooks for all 12 modules.

**Architecture:** Quick-win infrastructure first (CI, README, community files), then Rust cleanup, then the large content push (49 break/connect notebooks across 11 modules). Break/connect notebooks follow the Module 01 template: scenario → step-by-step code → cost analysis → the fix → exercises → summary.

**Tech Stack:** GitHub Actions (CI), SageMath (notebooks), Rust/Cargo (build/clippy), Markdown (docs)

---

## Phase 1: Infrastructure (quick wins)

### Task 1: Add GitHub Actions CI workflow

**Files:**
- Create: `.github/workflows/ci.yml`

**Step 1: Create the workflow file**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  rust:
    name: Rust build & clippy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
      - run: cargo build --workspace
      - run: cargo clippy --workspace -- -D warnings

  notebooks:
    name: Validate notebook JSON
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check all .ipynb files are valid JSON
        run: |
          find . -name '*.ipynb' -exec python3 -c "
          import json, sys
          with open(sys.argv[1]) as f:
              json.load(f)
          " {} \;
```

**Step 2: Verify the workflow is valid YAML**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`
Expected: No output (valid YAML). If `yaml` not installed, just verify manually.

**Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "Add CI workflow: Rust build/clippy + notebook JSON validation"
```

---

### Task 2: Silence Rust warnings for pedagogical stubs

The 189 warnings come from `todo!()` function parameters. Since these are intentional student exercises, prefix unused params with `_` and suppress dead-code warnings where needed.

**Files:**
- Modify: all 12 `rust/src/lib.rs` files

**Step 1: Add workspace-level lint config**

In root `Cargo.toml`, add after `[workspace.dependencies]`:

```toml
[workspace.lints.rust]
unused_variables = "allow"
dead_code = "allow"
unused_imports = "allow"
unused_mut = "allow"
```

Then in each module's `Cargo.toml`, add:

```toml
[lints]
workspace = true
```

**Step 2: Verify clean build**

Run: `cargo build --workspace 2>&1 | grep -c warning`
Expected: 0 (or close to 0)

Run: `cargo clippy --workspace 2>&1 | grep -c warning`
Expected: 0 (or close to 0)

**Step 3: Commit**

```bash
git add Cargo.toml foundations/*/rust/Cargo.toml frontier/*/rust/Cargo.toml
git commit -m "Suppress expected warnings from pedagogical todo!() stubs"
```

---

### Task 3: Add CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md`

**Step 1: Write the file**

Content should cover:
- How to report issues (bugs in notebooks, unclear explanations, wrong math)
- How to add content (new break/connect notebooks, new exercises)
- Style guide: micro-notebook principle, concrete-first, no logical jumps
- How to test: `cargo build --workspace`, open notebooks in SageMath
- PR process: one module per PR, describe what you changed and why

Keep it under 80 lines. Match the repo's warm, direct tone.

**Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "Add contributing guidelines"
```

---

### Task 4: Add GitHub issue templates

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug-report.md`
- Create: `.github/ISSUE_TEMPLATE/content-request.md`

**Step 1: Create bug report template**

```markdown
---
name: Bug Report
about: Something wrong in a notebook, README, or Rust exercise
labels: bug
---

**Module and file:**
<!-- e.g. Module 04, notebook 04c-euler-totient-fermats-theorem.ipynb -->

**What's wrong:**
<!-- Describe the error: wrong output, unclear explanation, broken code cell -->

**Expected behavior:**
<!-- What should happen instead -->
```

**Step 2: Create content request template**

```markdown
---
name: Content Request
about: Suggest a new notebook, exercise, or improvement
labels: enhancement
---

**Module:**
<!-- Which module does this relate to? -->

**What would you like to see:**
<!-- Describe the content: new break notebook, better visualization, etc. -->

**Why it matters:**
<!-- How does this help learners? -->
```

**Step 3: Commit**

```bash
git add .github/ISSUE_TEMPLATE/
git commit -m "Add GitHub issue templates for bugs and content requests"
```

---

### Task 5: Polish root README with badges and visual hook

**Files:**
- Modify: `README.md`

**Step 1: Add badges at the top**

After the `# Crypto From First Principles` heading, add:

```markdown
[![CI](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/USER/REPO/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
```

(Replace USER/REPO with actual GitHub path after first push.)

**Step 2: Add a "Quick Start" section**

After the philosophy section, before the module table, add a 3-line quick start:

```markdown
## Quick Start

```bash
git clone https://github.com/USER/REPO.git && cd REPO
conda activate sage && jupyter notebook foundations/01-modular-arithmetic-groups/sage/01a-integers-and-division.ipynb
```
```

**Step 3: Add a "Roadmap" section before License**

```markdown
## Roadmap

- [x] SageMath exploration notebooks (72 notebooks across 12 modules)
- [x] Scaffolded Rust exercises (57 functions with progressive difficulty)
- [x] Module 01 break/connect notebooks (4 attack + protocol notebooks)
- [ ] Break/connect notebooks for Modules 02-12
- [ ] Binder integration for zero-install browser experience
- [ ] Community-contributed exercises and visualizations
```

**Step 4: Commit**

```bash
git add README.md
git commit -m "Polish README: add badges, quick start, and roadmap"
```

---

### Task 6: Clean up stale files

**Files:**
- Modify: `.gitignore`
- Remove from tracking: `scripts/__pycache__/`

**Step 1: Add `__pycache__/` to .gitignore**

Append to `.gitignore`:
```
# Python
__pycache__/
**/__pycache__/
```

**Step 2: Clean up**

Run: `rm -rf scripts/__pycache__/`

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "Add __pycache__ to gitignore and clean up"
```

---

## Phase 2: Break/Connect Notebooks (large content push)

Each module needs 2-5 break/connect notebooks as described in its README. Follow the Module 01 pattern:

**Break notebook template:**
1. `# Break: [Attack Name]` + Module tag
2. "Why This Matters" section (1-2 paragraphs)
3. "The Scenario" with concrete small numbers
4. Step-by-step attack with SageMath code cells
5. Cost analysis comparing naive vs attack
6. "The Fix" showing the secure parameter choice
7. Exercises (2-3 variations)
8. Summary table + key takeaways
9. Navigation link back to module README

**Connect notebook template:**
1. `# Connect: [Protocol Name]` + Module tag
2. Introduction tracing module concepts to protocol
3. Concrete walkthrough with SageMath (small parameters)
4. "Concept Map" table: Module concept → Protocol application
5. "What's Next" pointing to later modules
6. Summary
7. Navigation link back to module README

### Task 7: Module 02 break/connect notebooks (4 notebooks)

**Files:**
- Create: `foundations/02-rings-fields-polynomials/break/reducible-polynomial-attack.ipynb`
- Create: `foundations/02-rings-fields-polynomials/break/zero-divisors-composite-n.ipynb`
- Create: `foundations/02-rings-fields-polynomials/connect/aes-gf256-arithmetic.ipynb`
- Create: `foundations/02-rings-fields-polynomials/connect/reed-solomon-codes.ipynb`

**README promises:**
- Break: Factor a "supposedly irreducible" polynomial to break a scheme built on a quotient ring
- Break: Find zero divisors in Z_n for composite n and show why Z_n fails to be a field
- Connect: AES uses GF(2^8), where all field arithmetic lives in a polynomial quotient ring
- Connect: Reed-Solomon error correcting codes rely on polynomial evaluation and interpolation over finite fields

**Step 1: Write all 4 notebooks following the templates above**

Each notebook should be 10-15 cells: 5-6 markdown cells interleaved with 4-5 SageMath code cells. Use concrete small examples (e.g., polynomials over GF(5), Z_12 for zero divisors).

**Step 2: Commit**

```bash
git add foundations/02-rings-fields-polynomials/break/ foundations/02-rings-fields-polynomials/connect/
git commit -m "Add Module 02 break/connect notebooks"
```

---

### Task 8: Module 03 break/connect notebooks (4 notebooks)

**Files:**
- Create: `foundations/03-galois-fields-aes/break/weak-sbox-reducible-poly.ipynb`
- Create: `foundations/03-galois-fields-aes/break/ecb-mode-pattern-leak.ipynb`
- Create: `foundations/03-galois-fields-aes/connect/aes-in-tls13.ipynb`
- Create: `foundations/03-galois-fields-aes/connect/aes-gcm-authentication.ipynb`

**README promises:**
- Break: Construct a weak S-box using a reducible polynomial and show the resulting algebraic vulnerability
- Break: Show why ECB mode leaks patterns by encrypting a structured image
- Connect: AES 128/256 in TLS 1.3 is the cipher suite that protects most web traffic
- Connect: AES-GCM authenticated encryption combines AES with Galois field based authentication

**Step 1: Write all 4 notebooks**
**Step 2: Commit**

```bash
git add foundations/03-galois-fields-aes/break/ foundations/03-galois-fields-aes/connect/
git commit -m "Add Module 03 break/connect notebooks"
```

---

### Task 9: Module 04 break/connect notebooks (5 notebooks)

**Files:**
- Create: `foundations/04-number-theory-rsa/break/hastads-broadcast-attack.ipynb`
- Create: `foundations/04-number-theory-rsa/break/wieners-attack-small-d.ipynb`
- Create: `foundations/04-number-theory-rsa/break/fermat-factorization-close-primes.ipynb`
- Create: `foundations/04-number-theory-rsa/connect/rsa-tls-certificates.ipynb`
- Create: `foundations/04-number-theory-rsa/connect/rsa-oaep-padding.ipynb`

**README promises:**
- Break: Hastad's broadcast attack (small e, no padding, multiple ciphertexts)
- Break: Wiener's attack on small d via continued fractions
- Break: Fermat factorization when |p - q| is small
- Connect: RSA in TLS certificates and PKCS#1
- Connect: RSA-OAEP padding in practice

**Step 1: Write all 5 notebooks**
**Step 2: Commit**

```bash
git add foundations/04-number-theory-rsa/break/ foundations/04-number-theory-rsa/connect/
git commit -m "Add Module 04 break/connect notebooks"
```

---

### Task 10: Module 05 break/connect notebooks (5 notebooks)

**Files:**
- Create: `foundations/05-discrete-log-diffie-hellman/break/small-subgroup-attack.ipynb`
- Create: `foundations/05-discrete-log-diffie-hellman/break/pohlig-hellman-smooth-order.ipynb`
- Create: `foundations/05-discrete-log-diffie-hellman/break/partial-bit-leakage.ipynb`
- Create: `foundations/05-discrete-log-diffie-hellman/connect/dh-in-tls13.ipynb`
- Create: `foundations/05-discrete-log-diffie-hellman/connect/signal-x3dh.ipynb`

**README promises:**
- Break: Small subgroup attack on DH with an unsafe prime
- Break: Pohlig-Hellman on a smooth order group
- Break: Recover a shared secret from leaked partial bits
- Connect: Diffie-Hellman in TLS 1.3 key exchange
- Connect: DH in the Signal protocol (X3DH)

**Step 1: Write all 5 notebooks**
**Step 2: Commit**

```bash
git add foundations/05-discrete-log-diffie-hellman/break/ foundations/05-discrete-log-diffie-hellman/connect/
git commit -m "Add Module 05 break/connect notebooks"
```

---

### Task 11: Module 06 break/connect notebooks (6 notebooks)

**Files:**
- Create: `foundations/06-elliptic-curves/break/ecdsa-nonce-reuse.ipynb`
- Create: `foundations/06-elliptic-curves/break/invalid-curve-attack.ipynb`
- Create: `foundations/06-elliptic-curves/break/twist-subgroup-attack.ipynb`
- Create: `foundations/06-elliptic-curves/connect/ecdh-x25519-tls13.ipynb`
- Create: `foundations/06-elliptic-curves/connect/ecdsa-bitcoin-ethereum.ipynb`
- Create: `foundations/06-elliptic-curves/connect/ed25519-ssh.ipynb`

**README promises:**
- Break: ECDSA nonce reuse (PlayStation 3 hack)
- Break: Invalid curve attack
- Break: Small subgroup on the twist
- Connect: ECDH (X25519) in TLS 1.3
- Connect: ECDSA in Bitcoin/Ethereum
- Connect: Ed25519 in SSH

**Step 1: Write all 6 notebooks**
**Step 2: Commit**

```bash
git add foundations/06-elliptic-curves/break/ foundations/06-elliptic-curves/connect/
git commit -m "Add Module 06 break/connect notebooks"
```

---

### Task 12: Module 07 break/connect notebooks (4 notebooks)

**Files:**
- Create: `frontier/07-pairings/break/rogue-key-attack-bls.ipynb`
- Create: `frontier/07-pairings/break/pairing-inversion-attempt.ipynb`
- Create: `frontier/07-pairings/connect/bls-ethereum-consensus.ipynb`
- Create: `frontier/07-pairings/connect/boneh-franklin-ibe.ipynb`

**README promises:**
- Break: Rogue key attack on naive BLS aggregation
- Break: Pairing inversion attempt
- Connect: BLS signatures in Ethereum 2.0 consensus
- Connect: Pairing based IBE (Boneh-Franklin)

**Step 1: Write all 4 notebooks**
**Step 2: Commit**

```bash
git add frontier/07-pairings/break/ frontier/07-pairings/connect/
git commit -m "Add Module 07 break/connect notebooks"
```

---

### Task 13: Module 08 break/connect notebooks (4 notebooks)

**Files:**
- Create: `frontier/08-lattices-post-quantum/break/lll-low-dimension-attack.ipynb`
- Create: `frontier/08-lattices-post-quantum/break/lwe-no-noise-recovery.ipynb`
- Create: `frontier/08-lattices-post-quantum/connect/nist-pqc-standards.ipynb`
- Create: `frontier/08-lattices-post-quantum/connect/hybrid-tls-post-quantum.ipynb`

**README promises:**
- Break: LLL attack on a low dimension lattice scheme
- Break: Recover LWE secret with no noise
- Connect: NIST PQC standards (ML-KEM, ML-DSA)
- Connect: Hybrid TLS with post-quantum

**Step 1: Write all 4 notebooks**
**Step 2: Commit**

```bash
git add frontier/08-lattices-post-quantum/break/ frontier/08-lattices-post-quantum/connect/
git commit -m "Add Module 08 break/connect notebooks"
```

---

### Task 14: Module 09 break/connect notebooks (4 notebooks)

**Files:**
- Create: `frontier/09-commitments-sigma-protocols/break/schnorr-nonce-reuse.ipynb`
- Create: `frontier/09-commitments-sigma-protocols/break/pedersen-unbounded-adversary.ipynb`
- Create: `frontier/09-commitments-sigma-protocols/connect/schnorr-bitcoin-taproot.ipynb`
- Create: `frontier/09-commitments-sigma-protocols/connect/commitments-in-zk-proofs.ipynb`

**README promises:**
- Break: Schnorr nonce reuse extracts secret key
- Break: Computationally unbounded adversary opens Pedersen commitment two ways
- Connect: Schnorr signatures in Bitcoin Taproot (BIP 340)
- Connect: Pedersen commitments in Bulletproofs, Groth16, polynomial commitments

**Step 1: Write all 4 notebooks**
**Step 2: Commit**

```bash
git add frontier/09-commitments-sigma-protocols/break/ frontier/09-commitments-sigma-protocols/connect/
git commit -m "Add Module 09 break/connect notebooks"
```

---

### Task 15: Module 10 break/connect notebooks (5 notebooks)

**Files:**
- Create: `frontier/10-snarks-starks/break/toxic-waste-forgery.ipynb`
- Create: `frontier/10-snarks-starks/break/malicious-crs-soundness.ipynb`
- Create: `frontier/10-snarks-starks/connect/groth16-zcash.ipynb`
- Create: `frontier/10-snarks-starks/connect/starks-starknet.ipynb`
- Create: `frontier/10-snarks-starks/connect/recursive-snarks-mina.ipynb`

**README promises:**
- Break: Forge a proof with compromised trusted setup
- Break: Soundness failure with bad CRS
- Connect: Groth16 in Zcash shielded transactions
- Connect: STARKs in StarkNet
- Connect: Recursive SNARKs in Mina

**Step 1: Write all 5 notebooks**
**Step 2: Commit**

```bash
git add frontier/10-snarks-starks/break/ frontier/10-snarks-starks/connect/
git commit -m "Add Module 10 break/connect notebooks"
```

---

### Task 16: Module 11 break/connect notebooks (5 notebooks)

**Files:**
- Create: `frontier/11-homomorphic-encryption/break/exhaust-noise-budget.ipynb`
- Create: `frontier/11-homomorphic-encryption/break/cpa-deterministic-encryption.ipynb`
- Create: `frontier/11-homomorphic-encryption/connect/fhe-private-ml.ipynb`
- Create: `frontier/11-homomorphic-encryption/connect/encrypted-databases.ipynb`
- Create: `frontier/11-homomorphic-encryption/connect/seal-google-fhe.ipynb`

**README promises:**
- Break: Exhaust noise budget in FHE
- Break: CPA attack on deterministic encryption
- Connect: FHE in privacy preserving ML
- Connect: Encrypted databases
- Connect: Microsoft SEAL and Google FHE compiler

**Step 1: Write all 5 notebooks**
**Step 2: Commit**

```bash
git add frontier/11-homomorphic-encryption/break/ frontier/11-homomorphic-encryption/connect/
git commit -m "Add Module 11 break/connect notebooks"
```

---

### Task 17: Module 12 break/connect notebooks (5 notebooks)

**Files:**
- Create: `frontier/12-mpc/break/cheating-dealer-detection.ipynb`
- Create: `frontier/12-mpc/break/corrupt-party-additive.ipynb`
- Create: `frontier/12-mpc/connect/threshold-wallets.ipynb`
- Create: `frontier/12-mpc/connect/private-set-intersection.ipynb`
- Create: `frontier/12-mpc/connect/secure-auctions.ipynb`

**README promises:**
- Break: Cheating dealer detection in Shamir sharing
- Break: Corrupt party in additive sharing
- Connect: Threshold wallets in cryptocurrency
- Connect: Private set intersection
- Connect: Secure auctions

**Step 1: Write all 5 notebooks**
**Step 2: Commit**

```bash
git add frontier/12-mpc/break/ frontier/12-mpc/connect/
git commit -m "Add Module 12 break/connect notebooks"
```

---

## Summary

| Phase | Tasks | Notebooks | Effort |
|-------|-------|-----------|--------|
| 1: Infrastructure | Tasks 1-6 | 0 | Small (30 min) |
| 2: Break/Connect | Tasks 7-17 | 47 notebooks | Large (one module at a time) |

**Total: 17 tasks, 47 new notebooks, 6 infrastructure files.**

After all tasks complete, the repo will have:
- Green CI badge
- 72 explore + 47 break/connect + 4 existing = **123 total notebooks**
- Clean `cargo build` with zero warnings
- Community-ready with CONTRIBUTING.md and issue templates
- Professional README with badges, quick start, and roadmap
