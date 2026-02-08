//! # Module 05: Discrete Logarithm and Diffie-Hellman — Exercises
//!
//! ## Progression
//! 1. `discrete_log_brute`   — Scaffolded (simple loop)
//! 2. `baby_step_giant_step` — Scaffolded (HashMap hint)
//! 3. `diffie_hellman`       — Independent
//! 4. `pohlig_hellman`       — Independent
//! 5. `is_safe_prime`        — Independent

use std::collections::HashMap;

/// Compute discrete log by brute force: find `x` such that `g^x ≡ h (mod p)`.
///
/// Returns `None` if no solution exists within `p - 1` steps.
pub fn discrete_log_brute(g: u64, h: u64, p: u64) -> Option<u64> {
    // Try x = 0, 1, 2, ... computing g^x mod p each time.
    // Hint: keep a running product instead of recomputing from scratch.
    todo!("Brute-force discrete log search")
}

/// Baby-step giant-step algorithm for discrete log.
///
/// Finds `x` such that `g^x ≡ h (mod p)`, where the group order is `n`.
/// Runs in O(√n) time and space.
///
/// Algorithm:
///   m = ceil(√n)
///   Baby steps: store g^j -> j for j = 0..m
///   Giant steps: for i = 0..m, check if h * (g^(-m))^i is in the table
pub fn baby_step_giant_step(g: u64, h: u64, p: u64, n: u64) -> Option<u64> {
    // Hint: use HashMap<u64, u64> for the baby step table.
    // You'll need mod_inverse of g^m to compute giant steps.
    todo!("BSGS discrete log in O(sqrt(n))")
}

/// Simulate a Diffie-Hellman key exchange.
///
/// Given generator `g` and prime `p`, and two secret keys `a` and `b`:
/// Returns `(A, B, shared)` where A = g^a mod p, B = g^b mod p,
/// and shared = g^(ab) mod p.
pub fn diffie_hellman(g: u64, p: u64, a: u64, b: u64) -> (u64, u64, u64) {
    todo!("DH key exchange: compute public keys and shared secret")
}

/// Pohlig-Hellman algorithm: solve DLP when the group order factors into small primes.
///
/// Given `g^x ≡ h (mod p)` and the factorization of the group order `n = p-1`,
/// solve the DLP in each prime-power subgroup and combine with CRT.
///
/// `factors` is a list of (prime, exponent) pairs such that n = ∏ p_i^e_i.
pub fn pohlig_hellman(
    g: u64,
    h: u64,
    p: u64,
    factors: &[(u64, u32)],
) -> u64 {
    todo!("Pohlig-Hellman: solve DLP via subgroup decomposition + CRT")
}

/// Check if `p` is a safe prime: `p` is prime and `(p-1)/2` is also prime.
///
/// Safe primes resist Pohlig-Hellman because (p-1) = 2 * q where q is a large prime.
pub fn is_safe_prime(p: u64) -> bool {
    todo!("Check if p and (p-1)/2 are both prime")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_discrete_log_brute() {
        // 3^x ≡ 6 (mod 7). Answer: x = 3 (3^3 = 27 ≡ 6)
        assert_eq!(discrete_log_brute(3, 6, 7), Some(3));
    }

    #[test]
    #[ignore]
    fn test_discrete_log_brute_identity() {
        // g^0 = 1 for any g
        assert_eq!(discrete_log_brute(5, 1, 13), Some(0));
    }

    #[test]
    #[ignore]
    fn test_bsgs() {
        // 2^x ≡ 3 (mod 5), order 4. Answer: x = 3
        assert_eq!(baby_step_giant_step(2, 3, 5, 4), Some(3));
    }

    #[test]
    #[ignore]
    fn test_diffie_hellman() {
        let (big_a, big_b, shared) = diffie_hellman(5, 23, 6, 15);
        assert_eq!(big_a, 8);  // 5^6 mod 23
        assert_eq!(big_b, 19); // 5^15 mod 23
        // Both sides compute the same shared secret
        // A^b = 8^15 mod 23 = B^a = 19^6 mod 23
        assert_eq!(shared, 2);
    }

    #[test]
    #[ignore]
    fn test_is_safe_prime() {
        assert!(is_safe_prime(23));  // (23-1)/2 = 11, both prime
        assert!(!is_safe_prime(37)); // (37-1)/2 = 18, not prime
    }
}
