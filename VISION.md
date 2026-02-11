# Crypto From First Principles — Vision 2026–2030

## Where We Are (v0.5, Feb 2026)

123 interactive SageMath notebooks, 57 Rust exercises, 12 modules spanning modular arithmetic to MPC. A four-stage pedagogy — **Explore → Implement → Break → Connect** — that bridges the gap between pure-math textbooks and black-box library tutorials. Binder integration for zero-install access.

The foundation is solid. This document lays out where to take it over the next 3–5 years.

---

## Core Thesis

Cryptography education is broken along a familiar fault line: you either drown in abstraction (Katz-Lindell, Boneh-Shoup) or you cargo-cult library calls. We already bridge that gap with notebooks and Rust. The next step is to **layer multiple representations of the same ideas** — visual intuition, formal rigor, interactive computation, verified proofs, and narrative video — so that every learner finds the entry point that clicks for them, and every learner is eventually pulled toward all the others.

In the LLM/agent era, the role of educational materials shifts. Students arrive with an AI that can generate code and regurgitate definitions. What they still can't get from an LLM is **deep structural intuition**, **verified correctness**, and **adversarial thinking**. Those are exactly the three things we double down on.

---

## The Six-Layer Module Architecture

Every module (01–12) grows from the current four-layer structure into six layers:

```
Module NN: <Topic>
├── lectures/
│   ├── part1-intuition/
│   │   ├── NN-intuition.excalidraw        # source (editable)
│   │   ├── NN-intuition.svg               # export for embedding
│   │   ├── NN-intuition.pdf               # export for printing/sharing
│   │   └── NN-intuition-notes.md          # speaker notes / oral script
│   └── part2-rigor/
│       ├── NN-rigor.tex                   # Beamer source
│       └── NN-rigor.pdf                   # compiled slides
├── video/
│   ├── NN-manim/                          # Manim animation source (polished)
│   └── NN-excalidraw-recording/           # Excalidraw screen-capture (lightweight)
├── sage/                                  # interactive exploration notebooks
├── rust/                                  # build-from-scratch exercises
├── break/                                 # attack weakened constructions
├── connect/                               # trace math into real protocols
└── lean4/                                 # formal verification of key theorems
```

### Why Six Layers, Not Four

The existing four layers (sage / rust / break / connect) are computation-centric. Students who learn best from **visual narrative** or from **formal proof** are underserved. The six-layer structure adds:

- **Lectures (Part 1 + Part 2):** The teacher's voice. Works for classroom adoption and self-study alike.
- **Lean4:** The machine-checked ground truth. Becomes the ultimate differentiator.

The video layer is a delivery format for the intuition layer, not a separate pedagogical stage.

---

## Layer 1: Excalidraw Intuition Slides

### What They Are

Hand-drawn-style visual explanations using Excalidraw. Each module gets a slide deck that answers: **"What's going on, and why should I care?"** No formal notation — just shapes, arrows, colors, and analogies.

### Design Principles

**Progressive revelation.** Excalidraw supports frames. Design each frame as one conceptual step. Example for Module 08 (Lattices):

- Frame 1 → A 2D lattice with basis vectors drawn boldly.
- Frame 2 → A target point appears. "Find the closest lattice point." (CVP)
- Frame 3 → Show the Voronoi cell. CVP = "which cell is the target in?"
- Frame 4 → Swap the basis for a "worse" one (nearly parallel). Same lattice, CVP now looks impossible visually.
- Frame 5 → This is why LLL matters: it finds a "nice" basis so CVP becomes tractable.

**Consistent color semantics across all 12 modules:**

| Color  | Meaning                        | Example                          |
|--------|--------------------------------|----------------------------------|
| Blue   | Public information             | Public key, group parameters     |
| Red    | Secret / private               | Private key, secret share        |
| Green  | Security assumption            | DLP is hard, LWE is hard        |
| Orange | Adversary's view / attack      | Eavesdropper, oracle queries     |
| Purple | Protocol flow / messages       | Commitment, challenge, response  |

**Cross-references to Part 2.** Annotate key diagrams with: "→ see Definition N.M in Part 2" or "→ notebook NNc". Beamer slides reciprocally embed thumbnail versions of key Excalidraw frames.

### Example: Module 09 (Commitments & Sigma Protocols)

- Envelope analogy: commitment = seal a value in an envelope (hiding); open the envelope and anyone can verify (binding).
- Pedersen commitment: two generators g, h drawn as arrows in "exponent space." C = g^m · h^r. The randomness r "smears" C across the group, hiding m.
- Schnorr protocol: two circles (Prover, Verifier), three arrows (commit → challenge → response). Annotate each arrow with what's being sent and why.
- Fiat-Shamir transform: replace the Verifier's challenge arrow with a hash-function icon. "The verifier got replaced by a hash."

### Tooling and Workflow

- `.excalidraw` files live in Git (JSON-based, diff-friendly).
- Export to SVG for web embedding, PDF for print/sharing.
- For video: record Excalidraw drawing process via OBS → lightweight "hand-drawing" video with voiceover. Lower production cost than Manim, arguably more authentic for conceptual content.

---

## Layer 2: Beamer Rigor Slides

### What They Are

LaTeX/Beamer slides in classic **Definition → Theorem → Proof** style. Each module gets a formal lecture deck that answers: **"What exactly did we just say, and why is it true?"**

### Design Principles

**Unified crypto macro package** (`crypto-macros.sty`) used across all 12 modules:

```latex
% Algorithms
\newcommand{\Setup}{\mathsf{Setup}}
\newcommand{\KeyGen}{\mathsf{KeyGen}}
\newcommand{\Enc}{\mathsf{Enc}}
\newcommand{\Dec}{\mathsf{Dec}}
\newcommand{\Sign}{\mathsf{Sign}}
\newcommand{\Verify}{\mathsf{Verify}}
\newcommand{\Commit}{\mathsf{Com}}
\newcommand{\Open}{\mathsf{Open}}

% Security
\newcommand{\Adv}{\mathcal{A}}
\newcommand{\Sim}{\mathcal{S}}
\newcommand{\negl}{\mathsf{negl}}
\newcommand{\poly}{\mathsf{poly}}
\newcommand{\AdvGame}[2]{\mathbf{Adv}^{#1}_{#2}}

% Groups and fields
\newcommand{\GG}{\mathbb{G}}
\newcommand{\FF}{\mathbb{F}}
\newcommand{\ZZ}{\mathbb{Z}}
\newcommand{\Zp}{\mathbb{Z}_p}

% Probability
\newcommand{\getsr}{\stackrel{\$}{\leftarrow}}
```

**Game-based security definitions** in standard two-column format (Challenger | Adversary), rendered with TikZ. Students see this format in Module 04 (IND-CPA for RSA) and encounter the same visual structure all the way through Module 12.

**Lean4 callout boxes.** After key theorems:

```
┌─────────────────────────────────────────────┐
│ ✓ Formalized: Lean4/Commit/Pedersen.lean    │
│   `theorem pedersen_hiding : ...`           │
└─────────────────────────────────────────────┘
```

**Excalidraw thumbnail references.** Before diving into formal definitions, include a small version of the relevant Excalidraw frame: "Recall this picture from Part 1. Now we make it precise."

### Content Scope per Module

Each Beamer deck should cover:

1. Formal definitions of the primitive(s) and their security notions.
2. The main construction(s) with correctness proofs.
3. Security reduction(s) — stated precisely, proved or proof-sketched.
4. Parameter guidance — concrete numbers, NIST recommendations where applicable.
5. Open problems or frontier connections (brief, 1–2 slides).

---

## Layer 3: Video (Two Formats)

### Format A: Manim Animations (High Polish)

3Blue1Brown-style. Best for topics where **continuous geometric transformation** is the key insight:

| Priority | Topic                           | Core Visual Idea                                                     |
|----------|---------------------------------|----------------------------------------------------------------------|
| 1        | Elliptic Curve Point Addition   | Real curve → chord-and-tangent → finite field "wrap" → ECDSA         |
| 2        | Lattice Basis Reduction         | 2D lattice, basis swap, LLL "shortening," CVP/SVP hardness          |
| 3        | Pairing Intuition               | Map from G₁×G₂ → G_T. "Lifting" DLP to a different group            |
| 4        | ZK: Schnorr to Groth16         | Interactive → Fiat-Shamir → arithmetization → R1CS → QAP            |
| 5        | FHE Bootstrapping               | Noise growth as a "filling glass," bootstrapping as "pouring it out" |
| 6        | Secret Sharing & MPC            | Shamir's scheme geometrically (points on a polynomial)               |

Target: **2–3 videos in Year 1**, growing to **8–10 by Year 2**.

### Format B: Excalidraw Recordings (Low Cost)

Screen-record the Part 1 Excalidraw slides being drawn, with voiceover. Authentic "whiteboard lecture" feel. Can cover every module quickly — this is how you get **12 modules of video content** without Manim production bottlenecks.

These two formats serve different purposes: Manim videos are *destination content* (people find them on YouTube and discover the project), Excalidraw recordings are *companion content* (students already in the course watch them alongside notebooks).

---

## Layer 4–6: Existing Layers (Enhanced)

### Layer 4: SageMath Notebooks (Explore)

Already strong. Enhancements:

- Add **AI tutor prompts** at the end of each notebook: a carefully engineered system prompt that turns Claude/GPT into a Socratic tutor for that specific topic. The prompt includes the module context, common misconceptions, and instructions to guide rather than answer directly.
- Add **"What if?" cells**: pre-written parameter variations that let students see what happens when they break assumptions (e.g., "What if p is not prime?" → watch the group structure collapse).

### Layer 5: Rust Exercises (Implement)

Already strong. Enhancements:

- **Progressive scaffolding labels**: tag each exercise as `guided` (loop skeleton given), `structured` (function signatures only), or `open` (just a spec). Currently implicit — make it explicit.
- **Property-based tests**: add `proptest` or `quickcheck` tests alongside unit tests. Students see that their implementation survives random inputs, not just known test vectors.
- **Benchmarking exercises**: in later modules, add `criterion` benchmarks so students can see the concrete cost of operations (e.g., pairing vs. scalar multiplication).

### Layer 6: Break + Connect Notebooks

Already strong. Enhancements:

- **Break notebooks get CTF-style scoring**: optional "flag" values that students compute by successfully breaking a weakened scheme.
- **Connect notebooks get live protocol traces**: use `tshark` or `openssl s_client` to capture real TLS handshakes and annotate them with the math from the module.

---

## Layer 7: Lean4 Formal Verification

### Why This Is the Long-Term Differentiator

As of 2026, no cryptography educational resource systematically formalizes its content in a proof assistant. Mathlib4 already has groups, rings, fields, polynomials, and basic number theory. The gap between Mathlib4 and "useful crypto formalization" is closable.

### What to Formalize (Phased)

**Phase 1 (Year 1–2): Algebraic Foundations**

Formalize the structures students build in Sage and Rust:

- Cyclic groups, generators, order, Lagrange's theorem.
- Ring and field axioms, polynomial rings, irreducibility.
- GF(p) and GF(2^n) arithmetic, with proofs that they satisfy field axioms.
- Euler's theorem, Fermat's little theorem, CRT.

These overlap heavily with Mathlib4 — the contribution is *pedagogical packaging*, not new math.

**Phase 2 (Year 2–3): Security Reductions**

This is where it gets novel:

- Formalize game-based security definitions (IND-CPA, IND-CCA, EUF-CMA) as Lean4 types.
- Formalize the RSA → factoring reduction.
- Formalize Pedersen commitment: perfectly hiding (information-theoretic) + computationally binding under DLP.
- Formalize Schnorr protocol: completeness, special soundness, HVZK.

**Phase 3 (Year 3–5): Frontier**

- Fiat-Shamir in the ROM (this is genuinely hard to formalize well).
- Groth16 soundness (would be a real academic contribution).
- LWE-based constructions and their reductions.

### Integration with the Learning Flow

Students don't write Lean4 from scratch (that's too steep a learning curve on top of crypto). Instead:

1. Read the theorem in Beamer (Part 2).
2. See the proof sketch on paper.
3. Open the Lean4 file and read the *formalized* version.
4. Fill in `sorry` gaps in guided exercises — like Rust `todo!()` but for proofs.
5. (Advanced) Write their own formalizations for exercises.

### LLM-Assisted Proof Search

This is an LLM-era superpower: students write the proof *structure* (key lemmas, reduction strategy), and an LLM helps fill in tactic-level details. This is pedagogically sound because the hard part of security proofs is the *structure*, not the mechanical steps.

---

## LLM & Agent Era Integration

### AI Tutor System

Each module ships with a tutor prompt file (`tutor-prompt.md`) designed to be pasted into Claude/ChatGPT. The prompt:

- Sets the Socratic mode: "Guide the student to discover the answer. Never give the solution directly."
- Includes module-specific context: definitions already covered, common misconceptions, prerequisite knowledge.
- Includes calibration examples: "If the student asks X, respond with Y (a hint), not Z (the answer)."

### Agent-Assisted Exercises

- **Lean4 tactic suggestions**: Student writes `sorry`, asks the AI "what tactic should I try here?", AI suggests based on the goal state.
- **Rust exercise hints**: AI can see the function signature and tests, provides incremental hints rather than full solutions.
- **Break challenge generation**: Given a scheme and parameter space, an LLM agent generates novel attack scenarios with known solutions.

### Interactive Protocol Simulation

For MPC modules (Module 12): an agent framework where students can "play" as one party in a multi-party protocol. The other parties are simulated by AI agents that follow the protocol honestly (or dishonestly, in the adversarial variant). The student sees messages arrive, decides what to send, and experiences the protocol as a participant rather than an observer.

---

## Community & Adoption Strategy

### Year 1: Visibility

- Release 2–3 Manim videos on YouTube. Target: elliptic curves, lattices, ZK. These are discovery engines.
- Start a Discord or Discourse for the community.
- Submit a talk to crypto/PL conferences (e.g., Real World Crypto, POPL) about the Lean4 angle.

### Year 2: University Adoption

- Package modules as drop-in supplements for existing courses. Target: 3–5 universities using the material.
- Create instructor guides: "How to use Module 06 in a one-semester crypto course."
- Beamer slides make this easy — professors can adopt them directly or fork them.

### Year 3–5: Self-Sustaining Ecosystem

- **Open textbook**: consolidate all content into a coherent book with cross-references. Think "Katz-Lindell meets 3Blue1Brown meets Software Foundations."
- **Community contributions**: modular structure allows external contributors to add exercises, visualizations, and Lean4 formalizations.
- **Industry partnerships**: crypto companies (protocol labs, ZK startups) sponsor modules relevant to their stack.

### Contribution Model

```
External contributor wants to add content
    │
    ├── New exercise?        → PR to rust/ or sage/ with tests
    ├── New visualization?   → PR to lectures/part1-intuition/
    ├── New Lean4 proof?     → PR to lean4/ with sorry-free build
    ├── New break challenge? → PR to break/ with known solution
    └── Translation?         → PR to i18n/<lang>/
```

---

## Concrete Milestones

### Year 1 (2026–2027)

- [ ] Excalidraw Part 1 slides for Modules 01–06 (Foundations)
- [ ] Beamer Part 2 slides for Modules 01–06
- [ ] 2–3 Manim videos (Elliptic Curves, Lattices, ZK intro)
- [ ] Excalidraw recording for every Foundation module
- [ ] Lean4 scaffold: formalize GF(p), cyclic groups, Lagrange's theorem
- [ ] `crypto-macros.sty` shared LaTeX macro package
- [ ] Tutor prompt files for Modules 01–06
- [ ] Community Discord/Discourse launch

### Year 2 (2027–2028)

- [ ] Excalidraw + Beamer for Modules 07–12 (Frontier)
- [ ] 5–7 more Manim videos (Pairings, FHE, MPC, Schnorr, Groth16)
- [ ] Lean4: game-based security definitions, RSA reduction, Pedersen
- [ ] University pilot: 3 courses using the material
- [ ] Conference talk on Lean4 crypto education
- [ ] Property-based tests and benchmarks for Rust exercises

### Year 3–5 (2028–2030)

- [ ] Lean4: Schnorr ZK properties, Fiat-Shamir ROM, LWE constructions
- [ ] Open textbook v1.0
- [ ] 15+ Manim videos (full YouTube series)
- [ ] Agent-based MPC simulation framework
- [ ] Internationalization (Chinese, Spanish at minimum)
- [ ] Lean4 frontier: Groth16 soundness formalization
- [ ] Self-sustaining community with regular external contributions

---

## Design Philosophy (Summary)

1. **Same idea, six representations.** Excalidraw gives geometric intuition. Beamer gives formal precision. SageMath lets you poke at it. Rust makes you build it. Break notebooks make you destroy it. Lean4 makes you prove it. No single representation is sufficient; together they cover the full spectrum from intuition to machine-checked certainty.

2. **LLMs handle the mechanical; humans handle the structural.** In the agent era, students don't need us to teach them syntax or simple derivations — they need us to teach them *why* a reduction works, *what* the right security definition is, and *how* to think like an adversary. Every layer is designed to exercise judgment, not recall.

3. **Progressive formalization.** Students start with pictures (Excalidraw), move to precise statements (Beamer), verify computationally (Sage/Rust), and ultimately machine-check (Lean4). This mirrors how working cryptographers actually think: sketch on a whiteboard, write it up formally, implement it, prove it correct.

4. **Modularity enables community.** Each module is self-contained enough for an external contributor to improve one layer without touching the others. A Lean4 expert can formalize Module 04 without knowing Manim. A visualization artist can improve Module 06's Excalidraw without knowing Rust.

---

*Last updated: February 2026. This is a living document — open an issue or start a Discussion to propose changes.*
