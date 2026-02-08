//! # Module 02: Rings, Fields, and Polynomials — Exercises
//!
//! Polynomials are `Vec<u64>` where index = degree: `vec![3, 0, 2]` = 2x² + 3.
//! All arithmetic is mod `p`.
//!
//! ## Progression
//! 1. `poly_eval`            — Guided (Horner's method skeleton)
//! 2. `poly_add`             — Guided (zip/pad approach)
//! 3. `poly_mul`             — Scaffolded (convolution hint)
//! 4. `poly_div_rem`         — Scaffolded (long division outline)
//! 5. `is_irreducible_mod_p` — Independent

/// Evaluate polynomial at `x` mod `p` using Horner's method.
///
/// # Example
/// ```
/// # use rings_fields_poly::poly_eval;
/// assert_eq!(poly_eval(&[1, 2, 3], 5, 7), 2); // 1 + 10 + 75 = 86 ≡ 2 mod 7
/// ```
pub fn poly_eval(coeffs: &[u64], x: u64, p: u64) -> u64 {
    // Horner's method: iterate from highest degree to lowest.
    //   result = 0
    //   for coeff in coeffs.iter().rev():
    //       result = (result * x + coeff) % p
    let mut result: u64 = 0;
    for &coeff in coeffs.iter().rev() {
        // TODO: result = (result * x + coeff) % p
        // Use u128 to avoid overflow.
        todo!("Horner step")
    }
    result
}

/// Add two polynomials coefficient-wise mod `p`. Trim trailing zeros.
pub fn poly_add(a: &[u64], b: &[u64], p: u64) -> Vec<u64> {
    // Hint: result length = max(a.len(), b.len())
    // Add corresponding coefficients mod p, then trim.
    todo!("Add polynomials mod p")
}

/// Multiply two polynomials mod `p` via convolution.
///
/// Coefficient of x^k = Σ a[i] * b[k-i] mod p for valid indices.
pub fn poly_mul(a: &[u64], b: &[u64], p: u64) -> Vec<u64> {
    todo!("Polynomial convolution mod p")
}

/// Polynomial long division: returns (quotient, remainder) mod `p`.
///
/// You'll need modular inverse of the leading coefficient of `b`.
pub fn poly_div_rem(a: &[u64], b: &[u64], p: u64) -> (Vec<u64>, Vec<u64>) {
    todo!("Polynomial long division mod p")
}

/// Check if polynomial is irreducible over Z/pZ by trial division.
///
/// Try all monic polynomials of degree 1..=deg/2. If none divide evenly,
/// the polynomial is irreducible.
pub fn is_irreducible_mod_p(coeffs: &[u64], p: u64) -> bool {
    todo!("Brute-force irreducibility check")
}

fn trim_poly(v: &mut Vec<u64>) {
    while v.len() > 1 && *v.last().unwrap() == 0 {
        v.pop();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_poly_eval_basic() {
        assert_eq!(poly_eval(&[1, 2, 3], 5, 7), 2);
    }

    #[test]
    #[ignore]
    fn test_poly_eval_constant() {
        assert_eq!(poly_eval(&[42], 999, 7), 0);
    }

    #[test]
    #[ignore]
    fn test_poly_add_same_degree() {
        assert_eq!(poly_add(&[1, 2, 3], &[4, 5, 6], 7), vec![5, 0, 2]);
    }

    #[test]
    #[ignore]
    fn test_poly_add_different_degree() {
        assert_eq!(poly_add(&[1, 2], &[3, 0, 1], 7), vec![4, 2, 1]);
    }

    #[test]
    #[ignore]
    fn test_poly_mul_linear() {
        assert_eq!(poly_mul(&[1, 1], &[1, 1], 7), vec![1, 2, 1]);
    }

    #[test]
    #[ignore]
    fn test_poly_mul_mod() {
        assert_eq!(poly_mul(&[3, 4], &[2, 5], 7), vec![6, 2, 6]);
    }

    #[test]
    #[ignore]
    fn test_poly_div_rem_exact() {
        let (q, r) = poly_div_rem(&[1, 2, 1], &[1, 1], 7);
        assert_eq!(q, vec![1, 1]);
        assert_eq!(r, vec![0]);
    }

    #[test]
    #[ignore]
    fn test_irreducible_true() {
        assert!(is_irreducible_mod_p(&[1, 1, 1], 2));
    }

    #[test]
    #[ignore]
    fn test_irreducible_false() {
        assert!(!is_irreducible_mod_p(&[1, 0, 1], 2));
    }
}
