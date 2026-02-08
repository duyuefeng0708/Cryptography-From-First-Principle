# Module 10: SNARKs and STARKs

Succinct proofs of computation — from arithmetic circuits to verifiable computation.

## Prerequisites

- [Module 06: Elliptic Curves](../../foundations/06-elliptic-curves/) — curve arithmetic needed for elliptic-curve-based SNARKs
- [Module 07: Bilinear Pairings](../07-pairings/) — pairing equations at the heart of Groth16
- [Module 09: Commitment Schemes and Sigma Protocols](../09-commitments-sigma-protocols/) — sigma protocol structure and the Fiat-Shamir transform

## Learning Objectives

After completing this module you will:
1. Understand arithmetic circuits and how to express computations as Rank-1 Constraint Systems (R1CS)
2. Construct a Quadratic Arithmetic Program (QAP) from an R1CS instance
3. Grasp the Groth16 proof system at a conceptual level — setup, prove, verify
4. Understand the FRI protocol and how STARKs achieve transparency without a trusted setup
5. Compare the trust assumptions, proof sizes, and verification costs of SNARKs vs STARKs

## Explore (SageMath Notebooks)

Work through these notebooks in order:

| # | Notebook | What You'll Learn |
|---|----------|-------------------|
| a | [Arithmetic Circuits](sage/10a-arithmetic-circuits.ipynb) | Representing computation as addition and multiplication gates over a field |
| b | [R1CS Constraints](sage/10b-r1cs-constraints.ipynb) | Flattening a circuit into A, B, C matrices and checking a witness |
| c | [QAP Construction](sage/10c-qap-construction.ipynb) | Interpolating R1CS into polynomials and the divisibility check |
| d | [Groth16 Overview](sage/10d-groth16-overview.ipynb) | Trusted setup, proving key, verification key, and the pairing check |
| e | [FRI Protocol](sage/10e-fri-protocol.ipynb) | Fast Reed-Solomon proximity testing via recursive folding |
| f | [STARKs vs SNARKs](sage/10f-starks-vs-snarks.ipynb) | Side-by-side comparison of trust model, proof size, and quantum resistance |

## Implement (Rust)

Build these from scratch in `rust/src/lib.rs`:

| # | Function | Description |
|---|----------|-------------|
| 1 | `evaluate_circuit` | Evaluate an arithmetic circuit on given inputs and return all wire values |
| 2 | `circuit_to_r1cs` | Convert a flat arithmetic circuit into R1CS matrices (A, B, C) |
| 3 | `check_r1cs_witness` | Verify that a witness vector satisfies Az * Bz = Cz element-wise |
| 4 | `fri_fold` | Perform one round of FRI folding on a polynomial evaluation domain |

Run: `cargo test -p snarks-starks`

## Break

Attack exercises in `break/`:
- **Forge a proof with compromised trusted setup** — given the toxic waste from a Groth16 ceremony, craft a valid proof for a false statement
- **Demonstrate soundness failure with bad CRS** — show that a malicious setup can produce a Common Reference String that lets anyone prove anything

## Connect

Real-world appearances in `connect/`:
- **Groth16 in Zcash shielded transactions** — every shielded spend and output is accompanied by a Groth16 proof of validity
- **STARKs in StarkNet** — StarkNet uses STARK proofs for ZK-rollup transaction validity on Ethereum
- **Recursive SNARKs in Mina** — Mina's blockchain stays a constant 22 KB by recursively verifying SNARK proofs of prior state

---
*Next: [Module 11: Homomorphic Encryption](../11-homomorphic-encryption/)*
