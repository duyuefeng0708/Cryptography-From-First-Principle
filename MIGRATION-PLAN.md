# Migration Plan: Dual Notebook Strategy (SageMath + Pure Python)

## Problem

SageMath on Binder takes 10+ minutes to build (conda env is ~2GB). This kills the "Try It Now" experience. But SageMath is genuinely powerful for advanced modules (pairings, lattice algorithms, elliptic curve internals). We don't want to lose that.

## Solution: Keep Both, Serve Different Audiences

```
Student clicks "Try It Now"
    │
    ├── Instant (< 5 sec) ──→ JupyterLite on GitHub Pages
    │                          Pure Python notebooks (sympy + custom lib)
    │                          Zero install, works on phone/tablet
    │
    └── Full power (~1 min) ──→ Codespaces / local Docker
                                SageMath notebooks (original)
                                + Rust toolchain + Lean4
```

Every SageMath notebook gets a **pure Python mirror**. Same pedagogy, same exercises, same outputs — different backend. The pure Python versions are first-class, not dumbed-down.

---

## Repository Structure (After Migration)

```
Module 01: Modular Arithmetic & Groups
├── sage/
│   ├── 01a-integers-and-division.ipynb          # SageMath kernel
│   ├── 01b-modular-arithmetic.ipynb
│   ├── 01c-groups-and-subgroups.ipynb
│   ├── 01d-cyclic-groups-generators.ipynb
│   ├── 01e-lagrange-theorem.ipynb
│   └── 01f-chinese-remainder-theorem.ipynb
├── python/
│   ├── 01a-integers-and-division.ipynb          # Python 3 kernel
│   ├── 01b-modular-arithmetic.ipynb
│   ├── 01c-groups-and-subgroups.ipynb
│   ├── 01d-cyclic-groups-generators.ipynb
│   ├── 01e-lagrange-theorem.ipynb
│   └── 01f-chinese-remainder-theorem.ipynb
├── rust/
├── break/
└── connect/
```

The `break/` and `connect/` notebooks also get Python mirrors where applicable.

---

## Shared Library: `cryptolab`

The pure Python notebooks import from a shared library that replaces SageMath primitives. This lives in `shared/cryptolab/` and is the backbone of the migration.

### Package Structure

```
shared/
└── cryptolab/
    ├── __init__.py
    ├── modular.py          # Mod(a, n), modular arithmetic
    ├── groups.py           # CyclicGroup, generators, order
    ├── fields.py           # GF(p), GF(2^n) with full arithmetic
    ├── poly.py             # Polynomial rings over finite fields
    ├── ec.py               # Elliptic curves, point addition, scalar mul
    ├── lattice.py          # Lattice, LLL (pedagogical), CVP/SVP
    ├── number_theory.py    # euler_phi, crt, legendre_symbol, etc.
    ├── pairing.py          # Weil/Tate pairing (simplified)
    ├── plot.py             # matplotlib wrappers matching SageMath plot style
    └── utils.py            # random primes, timing, display helpers
```

### Design Principles for `cryptolab`

1. **Readable over fast.** This is teaching code. A 30-line `__pow__` with square-and-multiply is better than calling `pow(a, e, n)` because students can step through it.

2. **API mirrors SageMath where possible.** Minimize cognitive load for anyone reading both versions.

   ```python
   # SageMath
   F = GF(17)
   a = F(3)
   a^(-1)

   # cryptolab — similar feel
   from cryptolab.fields import GF
   F = GF(17)
   a = F(3)
   a ** (-1)       # __pow__ handles negative exponents via Fermat
   ```

3. **Explicit internals.** Every class has a `_explain()` or verbose mode that prints what it's doing, step by step.

   ```python
   F = GF(17)
   a = F(3)
   a.pow_verbose(5)
   # Square-and-multiply for 3^5 mod 17:
   #   5 = 101 in binary
   #   bit 1: result = 3
   #   bit 0: square → 9
   #   bit 1: square → 81 → 13, multiply → 13 * 3 = 39 → 5
   #   Result: 5
   ```

4. **Pyodide-compatible.** No C extensions. Pure Python + numpy (available in Pyodide). sympy as optional dependency for symbolic display.

---

## Migration Phases

### Phase 0: Infrastructure (Week 1–2)

**Goal:** Set up the dual-track infrastructure before touching any notebooks.

- [ ] Create `shared/cryptolab/` package skeleton with `__init__.py`
- [ ] Set up JupyterLite config in `lite/` directory
- [ ] Create GitHub Actions workflow:
  ```yaml
  # .github/workflows/lite.yml
  - Build JupyterLite with contents from python/ directories
  - Deploy to GitHub Pages at Cryptography-From-First-Principle.github.io
  ```
- [ ] Create devcontainer.json for Codespaces:
  ```json
  {
    "image": "mcr.microsoft.com/devcontainers/python:3.12",
    "postCreateCommand": "pip install sympy matplotlib jupyterlab && conda install -c conda-forge sage",
    "features": {
      "ghcr.io/devcontainers/features/rust:1": {}
    }
  }
  ```
- [ ] Update README with two-tier "Try It Now" buttons:
  ```markdown
  [![Open in Browser](badge)](https://duyuefeng0708.github.io/Cryptography-From-First-Principle)  ← instant
  [![Open in Codespaces](badge)](https://codespaces.new/...)                        ← full env
  ```

### Phase 1: Foundation Modules 01–03 (Week 3–6)

These modules use the simplest SageMath features — mostly modular arithmetic, groups, and polynomial rings. Easiest to migrate.

**Module 01: Modular Arithmetic & Groups**

| SageMath construct             | cryptolab replacement                              | Complexity |
|--------------------------------|----------------------------------------------------|------------|
| `Integers(n)`, `Mod(a,n)`      | `cryptolab.modular.Mod(a, n)`                      | Simple     |
| `euler_phi(n)`                 | `cryptolab.number_theory.euler_phi(n)`              | Simple     |
| `factor(n)`                    | `sympy.factorint(n)`                                | Direct     |
| `multiplicative_order()`       | `Mod.order()` method                                | Simple     |
| `primitive_root(p)`            | `cryptolab.modular.primitive_root(p)`               | Simple     |
| Plots of group structure       | `cryptolab.plot.plot_group_cayley(G)`               | Medium     |

- [ ] Implement `cryptolab.modular` and `cryptolab.number_theory`
- [ ] Implement `cryptolab.plot` group visualization wrappers
- [ ] Mirror all 6 explore notebooks
- [ ] Mirror 2 break notebooks
- [ ] Mirror 2 connect notebooks
- [ ] Validate: outputs match between SageMath and Python versions
- [ ] Deploy to JupyterLite, smoke test

**Module 02: Rings, Fields & Polynomials**

| SageMath construct                        | cryptolab replacement                          | Complexity |
|-------------------------------------------|------------------------------------------------|------------|
| `PolynomialRing(GF(p), 'x')`             | `cryptolab.poly.PolyRing(GF(p))`              | Medium     |
| `R.irreducible_element(d)`               | `cryptolab.poly.find_irreducible(F, d)`        | Medium     |
| `f.is_irreducible()`                     | `sympy.polys.Poly.is_irreducible` or custom    | Medium     |
| `f.roots()`                              | `cryptolab.poly.find_roots(f, F)`              | Medium     |
| `R.quo(f)` (quotient ring)               | `cryptolab.fields.ExtensionField(p, poly)`     | Hard       |

- [ ] Implement `cryptolab.poly` with polynomial arithmetic over finite fields
- [ ] Implement `cryptolab.fields.GF` for prime fields
- [ ] Mirror all 6 + 2 + 2 notebooks
- [ ] Validate outputs

**Module 03: Galois Fields & AES**

| SageMath construct             | cryptolab replacement                         | Complexity |
|--------------------------------|-----------------------------------------------|------------|
| `GF(2^8, 'a', modulus=...)`   | `cryptolab.fields.GF(2, 8, modulus=...)`      | Hard       |
| AES S-box computation          | Pure Python (no SageMath needed)               | Simple     |
| `matrix(GF(2^8), ...)`        | numpy array + custom field arithmetic          | Medium     |

- [ ] Implement `cryptolab.fields.GF` for extension fields GF(p^n)
- [ ] Implement GF(2^8) operations (used heavily in AES module)
- [ ] Mirror all notebooks
- [ ] Validate: AES S-box values must match exactly

### Phase 2: Foundation Modules 04–06 (Week 7–12)

These are the most popular modules — RSA, DH, elliptic curves. High priority for JupyterLite access.

**Module 04: Number Theory & RSA**

| SageMath construct             | cryptolab replacement                         | Complexity |
|--------------------------------|-----------------------------------------------|------------|
| `is_prime(n)`                  | `sympy.isprime(n)`                             | Direct     |
| `random_prime(2^k)`           | `cryptolab.number_theory.random_prime(bits)`   | Simple     |
| `crt([a1,a2], [m1,m2])`      | `cryptolab.number_theory.crt(residues, moduli)`| Simple     |
| `power_mod(a, e, n)`          | `pow(a, e, n)` + verbose version               | Simple     |
| RSA key generation             | Pure Python (no SageMath needed)                | Simple     |

- [ ] Extend `cryptolab.number_theory` with CRT, primality, random primes
- [ ] Mirror all 6 + 3 + 2 notebooks
- [ ] Break notebooks: RSA with small e, common modulus, etc.

**Module 05: Discrete Log & Diffie-Hellman**

| SageMath construct             | cryptolab replacement                         | Complexity |
|--------------------------------|-----------------------------------------------|------------|
| `discrete_log(a, g, n)`       | `cryptolab.modular.baby_giant(g, a, n)`        | Medium     |
| DLP visualization              | `cryptolab.plot.plot_dlp_search(g, p)`         | Medium     |
| `Mod(g, p)` exponentiation     | Already in `cryptolab.modular`                  | Done       |

- [ ] Implement baby-step giant-step, Pollard's rho in `cryptolab`
- [ ] Mirror all notebooks

**Module 06: Elliptic Curves** ← most important for visibility

| SageMath construct                    | cryptolab replacement                      | Complexity |
|---------------------------------------|--------------------------------------------|------------|
| `EllipticCurve(GF(p), [a,b])`        | `cryptolab.ec.EllipticCurve(F, a, b)`      | Medium     |
| `E.points()`                          | `ec.all_points()` (enumerate)               | Simple     |
| `P + Q`, `n * P`                      | `Point.__add__`, `Point.__rmul__`           | Medium     |
| `E.order()`                           | Naive count or baby-step giant-step          | Medium     |
| `E.plot()`                            | `cryptolab.plot.plot_curve(E)` matplotlib    | Medium     |
| `E.abelian_group()`                   | Display group structure                      | Hard       |

- [ ] Implement `cryptolab.ec` with Weierstrass curves over GF(p)
- [ ] Point addition with full formulas (not library calls)
- [ ] Implement `plot_curve` for both real and finite field visualizations
- [ ] Mirror all 6 + 3 + 3 notebooks
- [ ] Validate: point counts, specific curve operations against SageMath

### Phase 3: Frontier Modules 07–12 (Week 13–24)

These are graduate-level. Migrating is harder but the audience is smaller and more tolerant of a local install.

**Module 07: Bilinear Pairings**

This is the hardest module to migrate. SageMath's pairing support is deep.

| SageMath construct               | cryptolab replacement                    | Complexity |
|----------------------------------|------------------------------------------|------------|
| `E.weil_pairing(P, Q, n)`       | `cryptolab.pairing.weil(P, Q, n)`        | Very Hard  |
| Miller's algorithm                | Pedagogical implementation in pure Python | Hard       |
| Embedding degree computation      | Custom                                    | Medium     |

Strategy: implement a **simplified** pairing over small curves for teaching purposes. Not production-grade — just enough to demonstrate the bilinear property and compute BLS signatures on toy parameters.

- [ ] Implement Miller's algorithm in pure Python
- [ ] Implement simplified Weil pairing
- [ ] Mirror notebooks (some may be "SageMath-only" if the pure Python version is too slow for the specific exercise)

**Modules 08–12: Lattices, Commitments, SNARKs, FHE, MPC**

These modules are less dependent on SageMath's specific algebra system and more on general Python:

| Module | SageMath dependency level | Migration difficulty |
|--------|--------------------------|---------------------|
| 08 Lattices | Medium (LLL, matrix ops) | Medium — numpy + custom LLL |
| 09 Commitments | Low (just group ops) | Easy — reuse cryptolab.modular |
| 10 SNARKs | Low (field arithmetic) | Easy — reuse cryptolab.fields |
| 11 FHE | Medium (polynomial rings) | Medium — reuse cryptolab.poly |
| 12 MPC | Low (secret sharing is simple) | Easy |

- [ ] Module 08: implement pedagogical LLL in pure Python + numpy
- [ ] Modules 09–12: mostly reuse existing cryptolab components
- [ ] Mark any notebook that *genuinely needs* SageMath as "SageMath-only" with a badge

---

## Notebook Conventions

### Header Cell (Every Python Notebook)

```python
# This notebook has two versions:
#   Python (this file) — runs in browser via JupyterLite, no install needed
#   SageMath (../sage/) — richer algebra system, needs local install or Codespaces
#
# Both versions cover the same material. Choose whichever works for you.

import sys
sys.path.insert(0, '../../shared')
from cryptolab.fields import GF
from cryptolab.plot import plot_group
```

### Compatibility Badges in Module README

```markdown
| Notebook                    | Python (browser) | SageMath |
|-----------------------------|:---:|:---:|
| 01a Integers and Division   | ✅  | ✅  |
| 01b Modular Arithmetic      | ✅  | ✅  |
| ...                         |     |     |
| 07c Weil Pairing Internals  | ⚠️ slow | ✅  |
| 07d Optimal Ate Pairing     | ❌ SageMath only | ✅  |
```

### Automated Equivalence Testing

CI runs both versions and checks outputs match:

```yaml
# .github/workflows/notebook-parity.yml
- name: Run Python notebook
  run: jupyter nbconvert --execute python/01a-*.ipynb --to notebook
- name: Run SageMath notebook
  run: sage -n jupyter --execute sage/01a-*.ipynb
- name: Compare outputs
  run: python scripts/compare-notebook-outputs.py python/01a-*.ipynb sage/01a-*.ipynb
```

This catches drift between the two versions.

---

## JupyterLite Deployment

### Config

```yaml
# lite/jupyter-lite.json
{
  "jupyter-lite-schema-version": 0,
  "jupyter-config-data": {
    "contentsStorageName": "Cryptography-From-First-Principle",
    "appName": "Crypto From First Principles"
  }
}
```

### Pre-install Packages

```yaml
# lite/requirements.txt (Pyodide packages)
sympy
matplotlib
numpy
```

The `cryptolab` package is bundled directly into the content directory (no pip install needed — just `sys.path` manipulation).

### Build & Deploy

```yaml
# .github/workflows/deploy-lite.yml
name: Deploy JupyterLite
on:
  push:
    branches: [main]
    paths: ['**/python/**', 'shared/**', 'lite/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Build JupyterLite
        run: |
          pip install jupyterlite-core jupyterlite-pyodide-kernel
          mkdir -p lite/files
          # Copy all Python notebooks and shared library
          cp -r foundations/*/python/ lite/files/foundations/
          cp -r frontier/*/python/ lite/files/frontier/
          cp -r shared/ lite/files/shared/
          jupyter lite build --lite-dir lite --output-dir _output

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: _output
```

---

## Timeline Summary

| Week  | Milestone                                          | Deliverable                              |
|-------|----------------------------------------------------|------------------------------------------|
| 1–2   | Infrastructure: JupyterLite, CI, devcontainer       | "Try in Browser" button works (empty)    |
| 3–4   | `cryptolab` core: modular, number_theory, fields(p) | Module 01 Python notebooks live          |
| 5–6   | `cryptolab`: poly, fields(p^n)                       | Modules 02–03 Python notebooks live      |
| 7–8   | `cryptolab`: ec, expanded number_theory              | Module 04–05 Python notebooks live       |
| 9–10  | `cryptolab`: ec plotting, ECDSA                      | Module 06 Python notebooks live          |
| 11–12 | Stabilize Foundations, notebook parity CI            | All 6 Foundation modules dual-track      |
| 13–16 | `cryptolab`: pairing (simplified), lattice + LLL     | Modules 07–08 Python notebooks           |
| 17–20 | Modules 09–12 (lighter SageMath dependency)          | All 12 modules dual-track                |
| 21–24 | Polish, edge cases, "SageMath-only" badges           | v1.0 of dual-track system                |

---

## Decision Log

| Decision | Rationale |
|----------|-----------|
| Keep SageMath as first-class | Pairings, advanced lattice ops, `abelian_group()` are too valuable to drop |
| Pure Python is primary for new users | 5-second browser launch vs 10-minute Binder build — this decides whether someone tries the project |
| `cryptolab` is pedagogical, not production | Readable > fast. Verbose modes. No C extensions. This is a teaching library. |
| JupyterLite over Binder | Static hosting (free, fast, reliable) vs container spinning (slow, rate-limited) |
| Codespaces over Binder for SageMath | ~1 min build vs ~10 min. Free tier is generous. |
| Notebook parity CI | Without automated checks, the two versions will inevitably drift apart |
| Some notebooks marked "SageMath-only" | Better to be honest than ship a broken Python version of Weil pairing |

---

*This plan is designed to be executed incrementally. Each phase delivers working value. You can stop after Phase 1 (Modules 01–03) and already have a dramatically better onboarding experience.*
