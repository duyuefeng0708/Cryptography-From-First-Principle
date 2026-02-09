# Star Attraction Improvements Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Maximize GitHub star/fork potential through social proof, discoverability, community features, and a comparison table that sells the repo on first scroll.

**Architecture:** Quick-win repo metadata and community features first, then content improvements (comparison table, social preview), then GitHub Pages as a landing site. Everything is independent — no task blocks another.

**Tech Stack:** GitHub CLI (`gh`), matplotlib (social preview), GitHub Actions (Pages), Markdown

---

## Task 1: Add comparison table to README

The competitive data is already researched. A "How does this compare?" table in the README lets visitors instantly see the value versus alternatives they already know.

**Files:**
- Modify: `README.md` (insert after "Why This Exists" section, before the images)

**Step 1: Add the comparison section**

Insert this block after the 4-bullet "Why This Exists" list and before the `<p align="center">` image block:

```markdown
### How does this compare?

| | This Repo | Cryptopals | CryptoHack | MoonMath | Boneh (Stanford) |
|---|:---:|:---:|:---:|:---:|:---:|
| Interactive notebooks | 123 | — | web-only | PDF | — |
| Math foundations | abstract algebra → ZK | — | some | excellent | excellent |
| Build from scratch | Rust | Python | Python | — | — |
| Visualizations | SageMath plots | — | some | — | — |
| Attack labs | 27 break notebooks | 48 challenges | 100+ challenges | — | — |
| Real protocol connections | TLS, Bitcoin, Signal, Zcash | — | — | Ethereum/ZK | — |
| Zero-install (Binder) | yes | — | yes (web) | — | — |
| Scope | groups → FHE/MPC | symmetric + basic PK | varied | algebra → ZK | broad theory |
```

**Step 2: Verify README renders**

Visually check the table alignment in the raw markdown.

**Step 3: Commit**

```bash
git add README.md
git commit -m "Add comparison table to README"
```

---

## Task 2: Generate and set social preview image

When someone shares the repo link on Twitter/Reddit/Discord/Slack, GitHub uses the social preview image (1280x640). Without one, it's a generic GitHub card. This is the single highest-impact visual for link sharing.

**Files:**
- Modify: `scripts/generate_readme_images.py` (add `generate_social_preview()` function)
- Create: `docs/images/social-preview.png`

**Step 1: Add social preview generator function**

Add a new function to `scripts/generate_readme_images.py` that creates a 1280x640 dark-themed image with:
- Title: "Crypto From First Principles"
- Subtitle: "123 notebooks | 57 Rust exercises | 12 modules"
- Tagline: "Learn the math. Build it in Rust. Break it. See it in the wild."
- A small elliptic curve sketch in the corner for visual flair
- Dark background matching the existing image style

**Step 2: Run the script**

Run: `python3 scripts/generate_readme_images.py`
Expected: `docs/images/social-preview.png` created, ~50-100KB

**Step 3: Upload as social preview via GitHub API**

```bash
gh api repos/duyuefeng0708/learn-cryptography --method PATCH \
  --input <(echo '{}') 2>/dev/null  # Note: social preview must be set via web UI
```

Note: GitHub API doesn't support social preview upload. Print instructions for the user to upload manually at `Settings > Social preview > Edit > Upload an image`.

**Step 4: Commit the image**

```bash
git add docs/images/social-preview.png scripts/generate_readme_images.py
git commit -m "Add social preview image for link sharing"
```

---

## Task 3: Enable GitHub Discussions

Discussions let visitors ask questions, share solutions, and request content without filing formal issues. Creates community signal that attracts more stars.

**Step 1: Enable via gh CLI**

```bash
gh repo edit --enable-discussions
```

**Step 2: Create a welcome discussion**

```bash
gh api repos/duyuefeng0708/learn-cryptography/discussions \
  -f title="Welcome! Introduce yourself" \
  -f body="Share your background and what brings you here. Are you a student? Researcher? Self-taught? Which module are you starting with?" \
  -f category_slug="general"
```

If the API call doesn't work, create manually via the web UI.

**Step 3: Add Discussions link to README**

Add a badge after the Binder badge:

```markdown
[![Discussions](https://img.shields.io/github/discussions/duyuefeng0708/learn-cryptography)](https://github.com/duyuefeng0708/learn-cryptography/discussions)
```

**Step 4: Commit**

```bash
git add README.md
git commit -m "Add GitHub Discussions badge to README"
```

---

## Task 4: Add PR template and community health files

Professional repos have these. They signal maturity and make contributing easier.

**Files:**
- Create: `.github/pull_request_template.md`
- Create: `SECURITY.md`

**Step 1: Create PR template**

```markdown
## What does this PR do?

<!-- One sentence summary -->

## Module(s) affected

<!-- e.g., Module 04 (Number Theory & RSA) -->

## Checklist

- [ ] Notebooks are valid JSON (`python3 -c "import json; json.load(open('file.ipynb'))"`)
- [ ] Rust code compiles (`cargo build --workspace`)
- [ ] No logical jumps — each cell follows naturally from the last
- [ ] Exercises have clear instructions
```

**Step 2: Create security policy**

```markdown
# Security Policy

## Scope

This is a teaching repository. The cryptographic implementations are deliberately simplified for learning and are NOT suitable for production use.

## Reporting

If you find an error in the mathematical content or a misleading security claim, please open an issue with the "bug" label.
```

**Step 3: Commit**

```bash
git add .github/pull_request_template.md SECURITY.md
git commit -m "Add PR template and security policy"
```

---

## Task 5: Create v1.0 GitHub release

A tagged release signals "production-ready" and shows up in GitHub feeds. People trust repos with releases more than repos without.

**Step 1: Tag and create release**

```bash
gh release create v1.0 \
  --title "v1.0 — All 12 modules complete" \
  --notes "$(cat <<'EOF'
## What's included

- **72 SageMath exploration notebooks** covering abstract algebra through MPC
- **55 break/connect notebooks** — attack weakened primitives, trace math to real protocols
- **57 scaffolded Rust exercises** with progressive difficulty
- **12 module READMEs** with prerequisites, objectives, and roadmaps
- **Binder integration** for zero-install browser experience
- **CI** with Rust build/clippy and notebook JSON validation

## Modules

**Foundations (BSc):** Modular Arithmetic, Rings & Fields, Galois Fields & AES, Number Theory & RSA, Discrete Log & DH, Elliptic Curves

**Frontier (Postgrad):** Pairings, Lattices & PQ, Commitments & Sigma Protocols, SNARKs & STARKs, FHE, MPC
EOF
)"
```

No commit needed — releases are metadata only.

---

## Task 6: Add nbviewer badges to module READMEs

nbviewer renders notebooks beautifully with all outputs. Even without pre-rendered outputs, nbviewer shows the code cells and markdown clearly. This gives visitors a "preview before clone" experience.

**Files:**
- Modify: all 12 module `README.md` files

**Step 1: Add nbviewer link to each module README**

At the top of each module README, after the title, add:

```markdown
[![View notebooks on nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/duyuefeng0708/learn-cryptography/tree/main/foundations/01-modular-arithmetic-groups/sage/)
```

Adjust the path for each module (foundations/01..., foundations/02..., frontier/07..., etc.).

**Step 2: Commit**

```bash
git add foundations/*/README.md frontier/*/README.md
git commit -m "Add nbviewer badges to all module READMEs"
```

---

## Task 7: Submit to awesome lists

This is manual but high-value. Each awesome list drives steady organic traffic.

**Step 1: Fork and PR to awesome-cryptography**

Repository: `sobolevn/awesome-cryptography`
Section: "Courses" or "Educational"
Entry:
```markdown
- [Crypto From First Principles](https://github.com/duyuefeng0708/learn-cryptography) - 123 interactive SageMath notebooks + Rust exercises covering abstract algebra through ZK proofs. Binder-ready.
```

**Step 2: Fork and PR to awesome-rust**

Repository: `rust-unofficial/awesome-rust`
Section: "Cryptography" or "Education"

**Step 3: Fork and PR to awesome-zero-knowledge-proofs**

Repository: `matter-labs/awesome-zero-knowledge-proofs`
Section: "Learning resources"

No commit needed — these are external PRs.

---

## Summary

| Task | Impact | Effort | Needs manual step? |
|------|--------|--------|--------------------|
| 1. Comparison table | High (convinces visitors) | 5 min | No |
| 2. Social preview | High (link sharing) | 10 min | Yes (upload via Settings) |
| 3. GitHub Discussions | Medium (community signal) | 5 min | Maybe (API may need web UI) |
| 4. PR template + SECURITY.md | Medium (repo maturity) | 5 min | No |
| 5. v1.0 release | Medium (trust signal) | 2 min | No |
| 6. nbviewer badges | Medium (preview experience) | 10 min | No |
| 7. Awesome list PRs | High (organic traffic) | 20 min | Yes (external PRs) |

**Total: 7 tasks. Tasks 1-6 are automatable. Task 7 requires manual PRs.**
