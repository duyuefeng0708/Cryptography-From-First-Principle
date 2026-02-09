//! # Module 10: SNARKs and STARKs — Exercises
//!
//! ## Progression
//! 1. `evaluate_circuit`  — signature + doc
//! 2. `circuit_to_r1cs`   — signature + doc
//! 3. `check_r1cs_witness` — signature + doc
//! 4. `fri_fold`          — signature only

/// A gate in an arithmetic circuit.
#[derive(Debug, Clone)]
pub enum Gate {
    /// Addition gate: output = left + right
    Add(usize, usize),
    /// Multiplication gate: output = left * right
    Mul(usize, usize),
    /// Constant gate: output = value
    Const(i64),
}

/// Evaluate an arithmetic circuit on given inputs.
///
/// `gates` defines the circuit. The first `num_inputs` wires are input wires.
/// Each subsequent gate takes wire indices as inputs and produces one output wire.
///
/// Returns the value of all wires (inputs + intermediate + output).
pub fn evaluate_circuit(gates: &[Gate], inputs: &[i64], modulus: i64) -> Vec<i64> {
    todo!("Evaluate each gate, building up wire values")
}

/// Convert a circuit to R1CS form: A * witness . B * witness = C * witness.
///
/// Returns matrices (A, B, C) where each row corresponds to a constraint
/// and the witness vector is [1, inputs..., intermediates..., output].
///
/// Each matrix is Vec<Vec<i64>> (rows × witness_size).
#[allow(clippy::type_complexity)]
pub fn circuit_to_r1cs(
    gates: &[Gate],
    num_inputs: usize,
) -> (Vec<Vec<i64>>, Vec<Vec<i64>>, Vec<Vec<i64>>) {
    todo!("Flatten circuit into R1CS matrices")
}

/// Check whether a witness satisfies an R1CS instance.
///
/// For each row i: (A[i] · w) * (B[i] · w) == C[i] · w  (mod modulus)
pub fn check_r1cs_witness(
    a: &[Vec<i64>],
    b: &[Vec<i64>],
    c: &[Vec<i64>],
    witness: &[i64],
    modulus: i64,
) -> bool {
    todo!("Verify (A·w) * (B·w) = (C·w) for each constraint")
}

/// One round of FRI folding: reduce polynomial degree by half.
///
/// Given evaluations of a polynomial p(x) at points {ω^i},
/// fold using challenge α:
///   p_new(x²) = (p(x) + p(-x))/2 + α * (p(x) - p(-x))/(2x)
///
/// Returns the folded evaluations (half the length).
pub fn fri_fold(evaluations: &[i64], challenge: i64, modulus: i64) -> Vec<i64> {
    todo!("FRI folding step: halve the polynomial degree")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_evaluate_circuit() {
        // Circuit: c = a * b + a
        // Wire 0: a (input), Wire 1: b (input)
        // Wire 2: a * b, Wire 3: (a*b) + a
        let gates = vec![Gate::Mul(0, 1), Gate::Add(2, 0)];
        let wires = evaluate_circuit(&gates, &[3, 5], 97);
        assert_eq!(wires[2], 15); // 3 * 5
        assert_eq!(wires[3], 18); // 15 + 3
    }

    #[test]
    #[ignore]
    fn test_check_r1cs_witness() {
        // Simple constraint: a * b = c
        let a = vec![vec![0, 1, 0, 0]]; // selects wire 1
        let b = vec![vec![0, 0, 1, 0]]; // selects wire 2
        let c = vec![vec![0, 0, 0, 1]]; // selects wire 3
        let witness = vec![1, 3, 5, 15]; // [1, a, b, c]
        assert!(check_r1cs_witness(&a, &b, &c, &witness, 97));
    }
}
