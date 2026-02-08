# Module 01: Modular Arithmetic & Groups — Content Fill Plan

## Context
The skeleton is complete (4 commits on main). Module 01 has 6 SageMath notebook stubs (11 cells each, thin content, TODO exercises/summaries), a scaffolded Rust lib.rs (5 functions, tests ready), and empty break/ and connect/ directories. We now fill everything with real teaching content.

**Core priority**: Narrow the understanding gap. The #1 reason students fail abstract algebra is the leap from "computing with numbers" to "reasoning about algebraic structures." Every cell must bridge that gap.

## Open Question: Do We Need a Phase 0?

### The Problem
Module 01 starts with "Integers and Division" — the division algorithm, remainders, `divmod()`. This is mathematically correct but **motivationally empty**. A student opening 01a asks: *"Why am I computing remainders? What does this have to do with cryptography?"*

### Candidates for Phase 0 Content

| Topic | Purpose | Verdict |
|-------|---------|---------|
| **Frequency analysis** (Caesar/Vigenere) | "Classical ciphers break easily → we need math" | **NO** — too disconnected from algebra; becomes its own module |
| **AES teaser** | "AES uses GF(256) → let's learn what fields are" | **NO** — Module 03 covers AES; a teaser here jumps too far ahead |
| **"Why math for crypto?" intro notebook** | Motivate the entire module in 10 minutes | **YES — but inline, not separate** |
| **XOR-based cipher demo** | "XOR = addition in GF(2) = mod 2 arithmetic" | **MAYBE** — elegant bridge from "crypto" to "mod arithmetic" |

### Recommendation: Embed Motivation, Don't Add a Phase

Rather than a separate Phase 0, **embed the motivation directly into 01a** as the opening section:

1. **Opening demo** (5 min): Show a toy XOR cipher. `message XOR key = ciphertext`. "XOR is addition mod 2. Every modern cipher is built on modular arithmetic." This gives the student a *reason* to care about remainders.

2. **Crypto foreshadowing** at the end of every notebook (already in the plan): each summary ends with a 2-line teaser connecting the math to RSA, DH, etc.

3. **Break/Connect notebooks** (Tasks 7-10) provide the deep crypto connections *after* the math is learned.

This avoids:
- A separate "Module 00" that bloats the repo and delays learning
- Frequency analysis (a classical topic that doesn't feed into algebra)
- AES teasers (Module 03's job, and requires fields which haven't been introduced)

### If You Still Want Phase 0

If a standalone motivation notebook is preferred, it would be:
- `00-why-algebra.ipynb` — 15 min, covers: (1) Caesar cipher → broken by frequency analysis in 3 lines of code, (2) "We need math to build ciphers that CAN'T be broken this way", (3) XOR cipher → "this is mod 2 arithmetic", (4) "Modules 01-06 build the math; Modules 07-12 apply it to frontier crypto."

---

## Gap-Narrowing Strategy

### Problem: Where students get lost
1. **"Why do I care about remainders?"** — 01a computes remainders but never motivates *why* we'd build a whole system around them
2. **"What IS a congruence class?"** — 01b jumps to `Zmod(n)` without showing that 2, 9, 16, 23... are "the same number"
3. **"Why are groups a thing?"** — 01c introduces axioms before students see *why* abstracting the pattern matters
4. **"Generator vs non-generator — so what?"** — 01d shows generators exist but doesn't show why they matter for crypto
5. **"Lagrange feels arbitrary"** — 01e states the theorem without building the "aha" moment
6. **"Pretty pictures but why?"** — 01f has visualizations disconnected from earlier concepts

### Solution: 5 pedagogical techniques applied to every notebook

1. **Motivating Question** — Each notebook opens with a concrete question the student can't yet answer. The notebook resolves it.
2. **Inline Checkpoints** — "Predict-then-verify" cells between sections: student predicts an output, runs code, confronts misconception.
3. **Misconception Callouts** — Explicit `> **Common mistake:**` blocks addressing known stumbling points.
4. **Bridge Paragraphs** — Between sections AND between notebooks: "In the last notebook we saw X. That naturally raises the question: Y."
5. **Crypto Foreshadowing** — Each notebook ends with a 2-line teaser connecting the math to a real crypto use case.

## Files to Modify/Create

```
foundations/01-modular-arithmetic-groups/
├── sage/01a-integers-and-division.ipynb          (modify)
├── sage/01b-modular-arithmetic.ipynb              (modify)
├── sage/01c-groups-first-look.ipynb               (modify)
├── sage/01d-cyclic-groups-generators.ipynb         (modify)
├── sage/01e-subgroups-lagrange.ipynb               (modify)
├── sage/01f-group-visualization.ipynb              (modify)
├── break/smooth-order-attack.ipynb                (create)
├── break/weak-generator-attack.ipynb              (create)
├── connect/rsa-key-generation.ipynb               (create)
├── connect/dh-parameter-selection.ipynb           (create)
└── rust/src/lib.rs                                (verify only)
```

## Task List (10 tasks, 2 commits)

### Phase 1: Notebook Content (6 tasks)

Target per notebook: ~20-25 cells (up from 11). Every notebook follows this enhanced structure:
- **Motivating question** (markdown) — a hook the student can't yet answer
- **Topic-specific objectives** (replace generic ones)
- **Bridge from previous notebook** (replace generic prerequisites)
- **Concept sections** with interleaved narrative → code → checkpoint pattern
- **Misconception callouts** (≥1 per notebook)
- **3 exercises** (faded: worked → guided → independent) with code cells for each
- **Summary** with crypto foreshadowing
- **Navigation link**

---

**Task 1: Fill 01a — Integers and Division**

*Motivating question*: "You send the message 42 to your friend, but you can only use numbers 0-6. How?"

*Bridge*: None (first notebook). Instead: "This module builds the math behind every encryption algorithm. We start with something you already know — division — and discover it hides a powerful structure."

*Content sections*:
1. **The division algorithm** — `37 ÷ 7`: show `divmod()`, then ask "what if we ONLY cared about the remainder?" Run `divmod(a, 7)` for a = 37, 44, 51 → all give remainder 2. "These numbers are the same mod 7."
2. **Remainder patterns** — Print `k mod 7` for k in 0..20. Checkpoint: "Before you run this: how many distinct values will appear? Predict, then run." After: "The remainders cycle. This isn't a coincidence — it's the division algorithm guaranteeing 0 ≤ r < 7."
3. **SageMath's `Mod()`** — Distinguish `37 % 7` (Python integer) from `Mod(37, 7)` (SageMath ring element). Show that `Mod(37, 7) + Mod(51, 7)` does arithmetic *in the remainder world*. This is the seed of modular arithmetic.

*Misconception callout*: "`Mod(37, 7)` is NOT just '37 % 7 = 2'. It creates a number that LIVES in the world of remainders mod 7. When you add two such numbers, you stay in that world. This distinction becomes critical in the next notebook."

*Exercises*:
1. **Worked**: Compute `divmod(1234, 17)`. Verify: q × 17 + r = 1234. Then compute `Mod(1234, 17)` and confirm the remainder matches. *(Provide full solution code and output.)*
2. **Guided**: Build a table: for each n in {5, 6, 7}, print `k mod n` for k = 0..20. *(Provide loop skeleton, student fills the `print` format string.)* Question: "For which n does every remainder appear equally often? Why?"
3. **Independent**: Without running code first — if `a mod 7 = 3` and `b mod 7 = 5`, what is `(a + b) mod 7`? What about `(a × b) mod 7`? Verify with SageMath. Then: does this work for any modulus n? Test with n = 12.

*Summary*:
- The division algorithm: a = qb + r with 0 ≤ r < b, and (q, r) are unique
- Remainders cycle with period n — this creates exactly n "bins"
- `Mod(a, n)` creates an element that lives in the remainder system — arithmetic "wraps around"
- *Crypto teaser*: "Every number in RSA lives in this remainder world. The modulus n is the product of two secret primes."

---

**Task 2: Fill 01b — Modular Arithmetic**

*Motivating question*: "In mod 12 arithmetic (a clock), 7 + 8 = 3. But can you always 'undo' addition? Can you always 'undo' multiplication?"

*Bridge*: "In 01a we saw that remainders mod n cycle and wrap around. Now let's take this seriously: what if remainders ARE the numbers, and we do all our arithmetic inside this system? Welcome to Z/nZ."

*Content sections*:
1. **Z/nZ as a number system** — `Zmod(7)` creates the ring. List elements. Show `R(3) + R(5)` gives `R(1)`. Checkpoint: "Predict `R(4) * R(3)` in Z/7Z before running." Explain: we're not reducing after multiplying, we're working *inside* a system where 7 = 0.
2. **Operation tables reveal structure** — Display `Zmod(7).addition_table('elements')` and `Zmod(7).multiplication_table('elements')`. Point out: addition table has every element in every row (Latin square). Multiplication table? "Look at the row for 0. Now look at the row for 1. What's different?"
3. **Zero divisors: when multiplication breaks** — `Zmod(12).multiplication_table('elements')`. "Find two non-zero elements whose product is 0." These are zero divisors. Checkpoint: "In Z/12Z, compute 3 × 4. Why is this bad? Could you 'divide by 3' if 3 × 4 = 0?" Connect: `gcd(3, 12) = 3 ≠ 1` — zero divisors exist exactly when gcd(a, n) > 1.
4. **Units: the elements that behave** — The units of Z/nZ are elements with multiplicative inverses. `[x for x in Zmod(12) if gcd(ZZ(x), 12) == 1]` → {1, 5, 7, 11}. Verify each has an inverse. `euler_phi(12)` = 4. "The units form their own self-contained system."

*Misconception callout*: "Z/nZ is NOT 'the integers with a mod operation stuck on.' It's a complete number system with its own rules. In Z/12Z, the number 3 has no multiplicative inverse — not because we haven't found it, but because it provably cannot exist (3 × 4 = 0 means 3 can't be cancelled)."

*Exercises*:
1. **Worked**: Build the multiplication table for Z/8Z. Identify all zero divisors. For each zero divisor a, find b ≠ 0 with a·b = 0, and verify gcd(a, 8) > 1. *(Full solution provided.)*
2. **Guided**: List the units of Z/15Z. For each unit u, find u⁻¹ using `Mod(u, 15)^(-1)`. *(Provide the loop skeleton, student fills the inverse computation.)* Verify: |units| = φ(15). Compute φ(15) by hand using φ(15) = 15·(1-1/3)·(1-1/5).
3. **Independent**: For each n from 2 to 20, compute the number of zero divisors in Z/nZ. For which n are there NO zero divisors? State a conjecture. Then test: does Z/1Z have zero divisors? Is Z/1Z even interesting?

*Summary*:
- Z/nZ is a complete number system with n elements where arithmetic wraps at n
- Zero divisors (a·b = 0 with a,b ≠ 0) exist when n is composite — they're elements with gcd(a,n) > 1
- Units (elements with inverses) are exactly the elements with gcd(a,n) = 1; there are φ(n) of them
- *Crypto teaser*: "RSA works in Z/nZ where n = p·q. The number of units φ(n) = (p-1)(q-1) is the secret that makes decryption possible."

---

**Task 3: Fill 01c — Groups: First Look**

*Motivating question*: "Z/7Z under addition has 7 elements and every equation a + x = b has a solution. (Z/7Z)* under multiplication has 6 elements and every equation a · x = b has a solution. These are completely different operations, but they share the same deep structure. What IS that structure?"

*Bridge*: "In 01b we discovered that Z/nZ has two interesting subsets: all elements (under addition) and units (under multiplication). Both let you combine elements and undo the operation. Let's extract the common pattern — this is where abstract algebra begins."

*Content sections*:
1. **Spotting the pattern** — Side-by-side: (Z/7Z, +) and (Z/7Z*, ×). For each, verify: closed? identity? every element invertible? associative? "Two different operations, same four properties. A SET + OPERATION + FOUR PROPERTIES = a group."
2. **The four axioms, concretely** — State each axiom with the Z/7Z example right next to it. Closure: `R(a) + R(b) in R` for all a,b. Identity: `R(0)` for addition, `R(1)` for multiplication. Inverses: `-R(a)` for addition, `R(a)^(-1)` for multiplication. Associativity: spot-check with a triple. Checkpoint: "Before I tell you — what is the identity for (Z/7Z*, ×)? What is the inverse of 3?"
3. **A non-example** — Is (Z/6Z, ×) a group? Check closure ✓, identity ✓ (1), associativity ✓. But inverses? `Mod(2, 6)^(-1)` → error! "2 has no inverse because gcd(2,6) = 2 ≠ 1. Not every set-with-operation is a group. The axioms are your checklist."
4. **Additive vs multiplicative** — (Z/nZ, +) is ALWAYS a group (for any n ≥ 1). (Z/nZ*, ×) is a group ONLY for units. When n is prime, Z/nZ* = {1, 2, ..., n-1} and has n-1 elements. "Prime moduli give us the biggest, cleanest multiplicative groups."

*Misconception callout*: "A group is NOT just a set of numbers. It's a set TOGETHER WITH an operation. The same set {1,2,3,4,5,6} can form a group under multiplication mod 7 but NOT under multiplication mod 12 (because 2×6 = 12 ≡ 0 leaves the set). Always specify both the set AND the operation."

*Exercises*:
1. **Worked**: Verify all 4 axioms for (Z/5Z, +). Identity = 0. Inverses: 1↔4, 2↔3, 0↔0. Closure: show addition table is a Latin square. *(Full verification code provided.)*
2. **Guided**: Check whether ({1, 2, 3, 4, 5, 6}, × mod 7) is a group. *(Provide a function skeleton `check_group_axioms(elements, operation, mod)` that the student fills in for each axiom.)*
3. **Independent**: Investigate ({0, 2, 4, 6, 8, 10}, + mod 12). Is this a group? If yes, prove each axiom. If no, identify the failing axiom. Then: what is this set really? (Hint: it's ⟨2⟩ in Z/12Z.)

*Summary*:
- A group = set + operation satisfying closure, associativity, identity, inverses
- (Z/nZ, +) is always a group; (Z/nZ*, ×) is a group of the φ(n) units
- When n is prime, (Z/nZ*, ×) has the maximum n-1 elements
- *Crypto teaser*: "Diffie-Hellman key exchange works inside (Z/pZ*, ×). The security depends on this group being large enough that brute force is impossible."

---

**Task 4: Fill 01d — Cyclic Groups and Generators**

*Motivating question*: "In (Z/7Z*, ×), start with 3. Compute 3, 3², 3³, 3⁴, 3⁵, 3⁶. You get {3, 2, 6, 4, 5, 1} — the ENTIRE group from a single element! But start with 2: 2, 2², 2³ = {2, 4, 1}. Only half the group. Why does 3 'reach everywhere' and 2 doesn't?"

*Bridge*: "We know (Z/7Z*, ×) is a group. But some elements are more powerful than others — they can regenerate the entire group by themselves. These are generators, and they're the cornerstone of Diffie-Hellman, ElGamal, and DSA."

*Content sections*:
1. **Powers trace out a path** — Compute `[g^k for k in range(1, 7)]` for every g in Z/7Z*. Display as a table. "Each row is the orbit of one element. Some orbits are the whole group, others are smaller loops." Checkpoint: "Look at the orbit of 6. It's {6, 1}. Can you predict the orbit length before computing? (Hint: 6 ≡ -1 mod 7.)"
2. **Order of an element** — `multiplicative_order()` in Sage. Build order table for Z/7Z*: {1→1, 2→3, 3→6, 4→3, 5→6, 6→2}. "Elements with order 6 = |G| are generators. Elements with smaller order generate subgroups." Checkpoint: "Predict the orders in Z/11Z* before computing. What divides 10?"
3. **Why generators matter** — If g generates G, then every element is g^k for some k. "Finding k given g^k is the DISCRETE LOGARITHM PROBLEM — the hard problem behind most of modern cryptography." Demo: In Z/7Z*, 3^x ≡ 5. Solution: x = 5 (since 3⁵ = 243 = 34×7+5). "Easy for |G| = 6. When |G| ≈ 2²⁵⁶, this is believed impossible."
4. **Counting generators** — There are exactly φ(p-1) generators of Z/pZ*. Compute for p = 7: φ(6) = 2, generators = {3, 5} ✓. For p = 13: φ(12) = 4, generators = {2, 6, 7, 11}. "When p-1 has lots of small factors, there are relatively fewer generators."

*Misconception callout*: "The order of an element is NOT its value. In Z/7Z*, element 2 has order 3, and element 3 has order 6. The order is the length of the cycle when you keep multiplying — it's a structural property, not a numerical one."

*Exercises*:
1. **Worked**: List all powers of 2 in Z/13Z*. Determine ord(2). Is 2 a generator? *(Full computation: 2¹=2, 2²=4, ..., 2¹²=1. Order = 12 = |Z/13Z*|, so yes, 2 is a generator.)*
2. **Guided**: Find all generators of Z/11Z*. *(Provide code to compute orders of all elements. Student identifies which have order = φ(11) = 10.)* Verify the count matches φ(10) = 4.
3. **Independent**: In Z/31Z*, how many generators exist? Find them all. Then: pick one generator g and verify that every non-identity element can be written as g^k for exactly one k in {1,...,30}. What is log_g(17)?

*Summary*:
- The order of g is the smallest k with g^k = 1; it always divides |G|
- g is a generator iff ord(g) = |G|; then every element = g^k for unique k
- There are exactly φ(|G|) generators; finding k from g^k is the discrete log problem
- *Crypto teaser*: "In Diffie-Hellman, Alice and Bob agree on a generator g of a huge group. Alice picks secret a, sends g^a. Bob picks secret b, sends g^b. They both compute g^(ab) — but an eavesdropper can't, because discrete log is hard."

---

**Task 5: Fill 01e — Subgroups and Lagrange's Theorem**

*Motivating question*: "In Z/12Z, the element 4 generates {0, 4, 8} — a group of size 3 inside a group of size 12. Could it have generated a group of size 5? Of size 7? What sizes are POSSIBLE?"

*Bridge*: "In 01d we saw that non-generators produce smaller cycles. These cycles are actually groups in their own right — subgroups. Lagrange's theorem says their sizes are brutally constrained: a subgroup's size MUST divide the group's size. This is arguably the most important theorem in elementary group theory."

*Content sections*:
1. **Subgroups by generation** — For each a in Z/12Z, compute ⟨a⟩ = {a, 2a, 3a, ...} until you loop back to 0. Show results as a table. Checkpoint: "Before computing — predict |⟨3⟩| in Z/12Z. (Hint: how many steps until 3k ≡ 0 mod 12?)" Answer: 12/gcd(3,12) = 4.
2. **Lagrange's theorem: the constraint** — State: if H is a subgroup of G, then |H| divides |G|. Verify for every subgroup just computed. "The possible subgroup sizes of Z/12Z are exactly the divisors of 12: {1, 2, 3, 4, 6, 12}. And every divisor actually appears!"
3. **Cosets: why Lagrange works** — The coset a + H = {a + h : h ∈ H}. Compute all cosets of ⟨4⟩ = {0, 4, 8} in Z/12Z: 0+H = {0,4,8}, 1+H = {1,5,9}, 2+H = {2,6,10}, 3+H = {3,7,11}. "Four cosets, each of size 3, perfectly partition the 12 elements. |G| = |H| × (number of cosets). This is Lagrange."
4. **Consequences for element order** — Since ⟨a⟩ is a subgroup, ord(a) divides |G|. "In a group of order 12, element orders can only be 1, 2, 3, 4, 6, or 12. Never 5, 7, 8, 9, 10, 11." Checkpoint: "What are the possible element orders in Z/15Z*? First find |Z/15Z*| = φ(15), then list its divisors."

*Misconception callout*: "Lagrange says |H| DIVIDES |G|, not that every divisor of |G| appears as a subgroup. For non-cyclic groups, some divisors may have no corresponding subgroup. But for cyclic groups like Z/nZ, every divisor d of n gives a subgroup of size d: it's ⟨n/d⟩."

*Exercises*:
1. **Worked**: Find ALL subgroups of (Z/12Z, +). For each, give a generator and list elements. Verify |H| divides 12 in every case. *(Full computation with table.)*
2. **Guided**: Compute the cosets of H = ⟨5⟩ in Z/15Z. *(Provide H computation, student writes the coset loop.)* Verify they partition Z/15Z. How many cosets? What is [G:H] (the index)?
3. **Independent**: In Z/pZ* where p = 31, the group has order 30. List all possible subgroup sizes. For each size d, find an element whose order is d. Is there always such an element? (Hint: Z/pZ* is cyclic.)

*Summary*:
- ⟨a⟩ = {a, 2a, ...} is always a subgroup; its size is |G|/gcd(a, |G|) for additive groups
- Lagrange's theorem: |H| divides |G|, so subgroup sizes are constrained to divisors
- Cosets partition G into equal-sized pieces: |G| = |H| × [G:H]
- *Crypto teaser*: "Lagrange's theorem is why safe primes matter. If p = 2q+1 with q prime, then Z/pZ* has only subgroups of order 1, 2, q, 2q. An attacker can't hide in a small subgroup."

---

**Task 6: Fill 01f — Group Visualization**

*Motivating question*: "You've computed orders, generators, subgroups, and cosets. But can you SEE them? A single picture can reveal structure that tables of numbers hide."

*Bridge*: "Everything in 01a-01e was symbolic: equations, tables, lists. Now we make it visual. You'll literally see why generators 'reach everywhere', how subgroups nest, and where symmetry hides."

*Content sections*:
1. **Cayley graph** — Build a directed graph for Z/6Z: nodes = elements, edge a→a+1 (generator 1). Plot with circular layout. "It's a cycle!" Then: Z/6Z with generator 2 — the graph decomposes into cosets of ⟨2⟩.
2. **Subgroup lattice** — Compute all subgroups of Z/12Z. Build a Hasse diagram using `Poset`. "The lattice mirrors the divisor lattice of 12."
3. **Multiplication table heatmap** — `matrix_plot()` on Z/7Z*. Color-code by value. "Notice the symmetry — the group is abelian."

*Misconception callout*: "A Cayley graph depends on the CHOICE OF GENERATOR, not just the group. Z/6Z with generator 1 is a hexagonal cycle; with generator 2 it decomposes into two triangles."

*Exercises*:
1. **Worked**: Draw the Cayley graph of Z/8Z with generator 3. Change to generator 2 — what happens?
2. **Guided**: Compare the subgroup lattice of Z/12Z and Z/8Z. Which has more subgroups?
3. **Independent**: Create a heatmap for Z/15Z*. Identify visual "blocks" and explain them.

*Summary*:
- Cayley graphs show how generators connect elements
- Subgroup lattices mirror the divisor lattice (for cyclic groups)
- Heatmaps make commutativity and subgroup structure visible
- *Crypto teaser*: "In EC cryptography, the 'group' is points on a curve. Visualizing EC group structure will be Module 06."

---

### Phase 2: Break & Connect Notebooks (4 tasks, all parallelizable)

**Task 7: Create break/smooth-order-attack.ipynb**
- Scenario: DH with a smooth-order prime (p-1 has only small factors)
- Step-by-step Pohlig-Hellman-style attack: factor p-1, reduce to small DLPs, CRT to combine
- Lesson: safe primes prevent this

**Task 8: Create break/weak-generator-attack.ipynb**
- Scenario: DH with an element of small order (not a generator)
- Key space shrinks, brute force trivial
- Lesson: always verify generator has full order

**Task 9: Create connect/rsa-key-generation.ipynb**
- Trace Module 01 → RSA: Z/nZ* is the RSA group, φ(n) = group size, exponentiation = mod_exp
- Small worked example (p=61, q=53)
- Preview Module 04

**Task 10: Create connect/dh-parameter-selection.ipynb**
- Trace Module 01 → DH: generator of Z/pZ* is DH base, order determines security
- Parameter validation, RFC 3526 mention
- Preview Module 05

---

### Phase 3: Verify and Commit

After Phase 1: validate notebooks as JSON, commit
After Phase 2: validate break/connect notebooks, commit

## Parallelism

```
Tasks 1-3 (01a, 01b, 01c)  ─┐
                              ├─→ commit 1
Tasks 4-6 (01d, 01e, 01f)  ─┘

Tasks 7-10 (break + connect) ─→ commit 2
```

## Notebook Editing Approach

Use `NotebookEdit` tool to replace/insert cells by cell ID. Each notebook currently has cells `cell-0` through `cell-10`. For new cells, use `edit_mode=insert` with `cell_id` to specify insertion point.
