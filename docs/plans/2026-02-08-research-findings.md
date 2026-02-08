# Research Findings: Current SOTA in Crypto Teaching

## Landscape Analysis

### 1. SEED Labs (Du Wenliang, Syracuse)
- **URL**: https://seedsecuritylabs.org
- **Crypto modules**: Only 8 labs — Secret-Key Encryption, RSA, PKI, TLS, MD5 Collision, Hash Length Extension, Padding Oracle, PRNG
- **Tools**: Python, OpenSSL CLI, Ubuntu VMs
- **Pedagogy**: Guided walkthrough → hands-on exercise in controlled VM
- **Strengths**: Reproducible environments, widely adopted (1180+ institutes), NSF-funded
- **Weaknesses**:
  - **Zero abstract algebra** — no groups, fields, rings, EC math. Students use OpenSSL as a black box
  - **Static labs with known answers** — solutions on GitHub, YouTube, ChatGPT everywhere
  - **No frontier crypto** — nothing on ZK, lattices, pairings, FHE, MPC
  - **No math→code bridge** — students never understand *why* RSA works, just *that* it works
  - **Heavy VM setup** — Docker/VirtualBox overhead before learning starts

### 2. Cryptopals (Matasano/NCC Group)
- **URL**: https://cryptopals.com
- **Structure**: 8 sets × 8 challenges = 56 total
- **Pedagogy**: "Learn by breaking" — implement attacks on real-world crypto
- **Tools**: Language-agnostic (mostly Python/Go solutions exist)
- **Strengths**:
  - Excellent attack-first pedagogy — builds intuition for why bad crypto fails
  - Progressive difficulty ramp
  - Covers practical attacks: ECB/CBC, padding oracle, Bleichenbacher, ECDSA nonce reuse
- **Weaknesses**:
  - **No math theory** — jumps straight to attacks without algebraic foundation
  - **No visualization** — pure text challenges
  - **No interactive notebooks** — just problem descriptions
  - **Big difficulty jumps** between sets (especially set 5→6)
  - **No guidance on tooling** — students waste time on setup
  - **Stale** — no new challenges in years

### 3. CryptoHack
- **URL**: https://cryptohack.org
- **Structure**: 12 categories, CTF-style, 5 structured courses (Intro, Modular Arithmetic, Symmetric, Public-Key, Elliptic Curves)
- **Pedagogy**: Gamified learn-by-breaking, points/trophies/leaderboard
- **Tools**: Web-based, Python-centric
- **Strengths**:
  - Best gamification in crypto education
  - Covers lattices, isogenies, ZK (some frontier topics)
  - Active community, new challenges added
  - Modular arithmetic course exists (rare!)
- **Weaknesses**:
  - **Web-only** — no local notebooks, can't run offline
  - **No Rust** — Python only
  - **No systematic math progression** — jumps from modular arithmetic to RSA
  - **No implementation phase** — only breaking, never building from scratch
  - **No visualization** of algebraic structures
  - **No real-protocol connections**

### 4. MoonMath Manual (Least Authority)
- **URL**: https://github.com/LeastAuthority/moonmath-manual
- **Structure**: LaTeX textbook, pen-and-paper exercises
- **Coverage**: Groups → Rings → Fields → Elliptic Curves → Pairings → zk-SNARKs
- **Tools**: SageMath (via sagetex), pen-and-paper primary
- **Strengths**:
  - **Best math→ZK bridge** — builds from basic algebra to SNARKs
  - Pen-and-paper approach forces understanding
  - SageMath integration for verification
  - Used by ZK Hack study groups
- **Weaknesses**:
  - **Narrow scope** — only targets zk-SNARKs, not broader crypto
  - **No code implementation** — pen-and-paper, no Rust/production code
  - **PDF/LaTeX** — not interactive notebooks
  - **No "break it" exercises** — purely constructive
  - **No beginner on-ramp** — assumes some math maturity

### 5. Dan Boneh's Course (Stanford/Coursera)
- **URL**: https://crypto.stanford.edu/~dabo/courses/OnlineCrypto/
- **Textbook**: "A Graduate Course in Applied Cryptography" (free, v0.6)
- **Pedagogy**: Lecture → textbook → problem sets
- **Strengths**: Rigorous, covers broad topics, free textbook
- **Weaknesses**: No interactive code, no notebooks, lecture-heavy, no Rust

### 6. Uncloak
- **URL**: https://github.com/thor314/uncloak
- **Status**: Early stage, community wiki for crypto+Rust
- **Strengths**: Rust-focused, ZK-oriented
- **Weaknesses**: Incomplete, most pages under construction, no structured curriculum

## Tool Assessment

### SageMath for Teaching
- **Verdict: Excellent choice**
- Version 10.x stable, active development
- First-class support: `GF()`, `EllipticCurve()`, `PolynomialRing()`, `matrix().LLL()`
- Jupyter integration mature (SageMath kernel)
- Used by MoonMath Manual itself
- Book exists: "Learning and Experiencing Cryptography with CrypTool and SageMath"

### evcxr (Rust Jupyter Kernel)
- **Verdict: NOT mature enough as primary teaching tool**
- Can't interrupt running kernels (Rust threads)
- Async support broken (stuck on pre-1.0 tokio)
- API explicitly "very not stable"
- Long programs are poor experience in notebooks
- **Decision: Use Rust as standalone projects, NOT in Jupyter**

## Pedagogical Research

### Key Stumbling Blocks for CS Students in Abstract Algebra
1. **Abstraction barrier** — can't visualize groups/fields, stuck in concrete thinking
2. **Notation overload** — mathematical notation is a foreign language
3. **Unmotivated definitions** — "why do I care about group axioms?"
4. **Big conceptual jumps** — modular arithmetic → abstract groups is a cliff
5. **Procedure without understanding** — typing into CAS without knowing what they're doing

### What Works (Research-backed)
1. **APOS Framework** (Action → Process → Object → Schema) — gradual abstraction
2. **Concrete-first** — always start with specific examples (Z_7) before abstractions (group G)
3. **Visualization** — geometric representations of group operations, EC point addition
4. **Computer algebra as exploratory tool** — BUT obstacles must be made explicit
5. **Scaffolding** — gradually remove training wheels, small steps
6. **"Obstacles are opportunities"** — when students struggle with code, they learn conceptually

## Gap Analysis: How We Exceed SOTA

| Dimension | Current Best | Who | Our Approach | Improvement |
|-----------|-------------|-----|-------------|-------------|
| Math foundation | Pen-and-paper exercises | MoonMath | Interactive SageMath notebooks with visualization | Explore → see → understand |
| Attack exercises | CTF-style challenges | CryptoHack/Cryptopals | "Break" phase in every module | Attacks motivated by the math just learned |
| Implementation | None systematic | — | Rust from scratch, every module | Build real crypto, not use libraries |
| Progression | Big jumps | All | Micro-notebooks, one concept each | No logical leaps |
| Real protocol bridge | None | — | "Connect" phase linking to TLS/Signal/Zcash | Theory meets reality |
| Visualization | Almost none | — | First-class plots in Sage notebooks | See the algebra |
| Extensibility | Fixed sets | All | Numbered sub-notebooks, easy insertion | Community can add 01a, 01b between 01, 02 |
| Dynamic problems | None | — | LLM-generated unique parameters (future) | Anti-cheating |
| Tool bridge | One language | All | SageMath (explore) + Rust (implement) | Right tool for right job |
| Scope | Either basics OR frontier | All | BSc foundations → postgrad frontier in one repo | Complete pipeline |
| Beginner gap | Wide | All | Micro-steps, concrete-first, APOS-inspired | Smallest possible jumps |
