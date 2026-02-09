//! # Module 01: Modular Arithmetic and Groups — Exercises
//!
//! Work through these after completing the SageMath notebooks.
//! Implement each function, then remove `#[ignore]` from its tests to verify.
//!
//! ## Progression
//! 1. `mod_exp`             — Guided (loop structure provided)
//! 2. `gcd`                 — Guided (algorithm outline provided)
//! 3. `is_generator`        — Scaffolded (signature + hints)
//! 4. `element_order`       — Scaffolded (signature + hints)
//! 5. `find_all_generators` — Independent (just the signature)

/// Compute `base^exp mod modulus` using repeated squaring.
///
/// # Example
/// ```
/// # use mod_arith_groups::mod_exp;
/// assert_eq!(mod_exp(2, 10, 1000), 24);
/// ```
pub fn mod_exp(base: u64, exp: u64, modulus: u64) -> u64 {
    // Square-and-multiply algorithm:
    //   result = 1, base = base % modulus
    //   While exp > 0:
    //     if exp is odd: result = result * base mod modulus
    //     exp = exp / 2
    //     base = base * base mod modulus
    //
    // Watch out for overflow: cast to u128 before multiplying.
    let mut result: u64 = 1;
    let mut base = base % modulus;
    let mut exp = exp;
    while exp > 0 {
        if exp % 2 == 1 {
            // TODO: multiply result by base (mod modulus)
            todo!("result = result * base mod modulus")
        }
        exp /= 2;
        // TODO: square base (mod modulus)
        todo!("base = base * base mod modulus")
    }
    result
}

/// Compute gcd(a, b) using the Euclidean algorithm.
///
/// # Example
/// ```
/// # use mod_arith_groups::gcd;
/// assert_eq!(gcd(48, 18), 6);
/// ```
pub fn gcd(a: u64, b: u64) -> u64 {
    // Euclidean algorithm:
    //   while b != 0: (a, b) = (b, a % b)
    //   return a
    let mut a = a;
    let mut b = b;
    loop {
        if b == 0 {
            return a;
        }
        // TODO: one step — set (a, b) = (b, a % b)
        todo!("Update a and b")
    }
}

/// Check whether `g` is a generator of (Z/pZ)*.
///
/// `g` is a generator iff for every prime factor `q` of `p - 1`,
/// `g^((p-1)/q) ≢ 1 (mod p)`.
///
/// Assume `p` is prime.
pub fn is_generator(g: u64, p: u64) -> bool {
    // Hint: first find the prime factors of p - 1.
    // Then for each factor q, check that mod_exp(g, (p-1)/q, p) != 1.
    todo!("Check if g generates (Z/pZ)*")
}

/// Compute the multiplicative order of `a` in (Z/nZ)*.
///
/// Returns `None` if gcd(a, n) != 1 (a is not in the group).
///
/// Hint: try successive powers of `a` until you reach 1.
pub fn element_order(a: u64, n: u64) -> Option<u64> {
    // Hint: if gcd(a, n) != 1, return None.
    // Otherwise, compute a, a^2, a^3, ... mod n until you get 1.
    todo!("Find the smallest k where a^k ≡ 1 (mod n)")
}

/// Find all generators of (Z/pZ)*, returned as a sorted Vec.
///
/// Assume `p` is prime. There are exactly φ(p-1) generators.
pub fn find_all_generators(p: u64) -> Vec<u64> {
    todo!("Return all generators of (Z/pZ)*")
}

#[cfg(test)]
mod tests {
    use super::*;

    // ── mod_exp ──

    #[test]
    #[ignore]
    fn test_mod_exp_basic() {
        assert_eq!(mod_exp(2, 10, 1000), 24);
    }

    #[test]
    #[ignore]
    fn test_mod_exp_large() {
        assert_eq!(mod_exp(3, 100, 1_000_000_007), 981_147_432);
    }

    #[test]
    #[ignore]
    fn test_mod_exp_edge_cases() {
        assert_eq!(mod_exp(5, 0, 13), 1);
        assert_eq!(mod_exp(0, 5, 13), 0);
    }

    // ── gcd ──

    #[test]
    #[ignore]
    fn test_gcd_basic() {
        assert_eq!(gcd(48, 18), 6);
        assert_eq!(gcd(100, 75), 25);
    }

    #[test]
    #[ignore]
    fn test_gcd_coprime() {
        assert_eq!(gcd(17, 13), 1);
    }

    #[test]
    #[ignore]
    fn test_gcd_with_zero() {
        assert_eq!(gcd(42, 0), 42);
        assert_eq!(gcd(0, 42), 42);
    }

    // ── is_generator ──

    #[test]
    #[ignore]
    fn test_is_generator_true() {
        assert!(is_generator(3, 7));
    }

    #[test]
    #[ignore]
    fn test_is_generator_false() {
        assert!(!is_generator(2, 7));
    }

    // ── element_order ──

    #[test]
    #[ignore]
    fn test_element_order_generator() {
        assert_eq!(element_order(3, 7), Some(6));
    }

    #[test]
    #[ignore]
    fn test_element_order_non_generator() {
        assert_eq!(element_order(2, 7), Some(3));
    }

    #[test]
    #[ignore]
    fn test_element_order_not_in_group() {
        assert_eq!(element_order(4, 8), None);
    }

    // ── find_all_generators ──

    #[test]
    #[ignore]
    fn test_find_all_generators_7() {
        assert_eq!(find_all_generators(7), vec![3, 5]);
    }

    #[test]
    #[ignore]
    fn test_find_all_generators_13() {
        assert_eq!(find_all_generators(13), vec![2, 6, 7, 11]);
    }
}
