//! # Module 12: Multi-Party Computation — Exercises
//!
//! ## Progression
//! 1. `shamir_share`          — signature + doc
//! 2. `shamir_reconstruct`    — signature + doc
//! 3. `additive_share`        — signature + doc
//! 4. `additive_reconstruct`  — signature + doc
//! 5. `beaver_triple_mul`     — signature only

/// Create Shamir secret shares for a given secret.
///
/// Constructs a random polynomial f of degree `t - 1` where f(0) = secret,
/// then evaluates at points 1, 2, ..., n.
///
/// Returns `n` shares as (x, y) pairs.
///
/// - `t`: threshold (minimum shares needed to reconstruct)
/// - `n`: total number of shares
/// - `prime`: field modulus (must be > secret and > n)
pub fn shamir_share(secret: u64, t: usize, n: usize, prime: u64) -> Vec<(u64, u64)> {
    todo!("Generate Shamir secret shares using random polynomial")
}

/// Reconstruct a secret from `t` or more Shamir shares using Lagrange interpolation.
///
/// Evaluates the Lagrange interpolating polynomial at x = 0.
pub fn shamir_reconstruct(shares: &[(u64, u64)], prime: u64) -> u64 {
    todo!("Lagrange interpolation at x=0 to recover secret")
}

/// Create additive secret shares: split `secret` into `n` random shares
/// that sum to `secret` (mod 2^64).
pub fn additive_share(secret: u64, n: usize) -> Vec<u64> {
    todo!("Random additive shares summing to secret")
}

/// Reconstruct a secret from additive shares: just sum them.
pub fn additive_reconstruct(shares: &[u64]) -> u64 {
    todo!("Sum all shares (wrapping)")
}

/// Beaver triple-based multiplication of shared values.
///
/// Given:
/// - Party's share of `a` and `b` (the values to multiply)
/// - A pre-computed Beaver triple share `(u, v, w)` where u*v = w
/// - `p`: field modulus
///
/// The protocol:
/// 1. Compute d = a - u, e = b - v (open these)
/// 2. Party's share of a*b = w + e*u + d*v + d*e
///
/// Here we simulate a single party's computation given opened d and e.
pub fn beaver_triple_mul(
    a_share: u64,
    b_share: u64,
    u_share: u64,
    v_share: u64,
    w_share: u64,
    d: u64,
    e: u64,
    p: u64,
) -> u64 {
    todo!("Compute party's share of a*b using Beaver triple")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_shamir_roundtrip() {
        let secret = 42_u64;
        let shares = shamir_share(secret, 3, 5, 97);
        assert_eq!(shares.len(), 5);
        // Any 3 shares should reconstruct the secret
        let reconstructed = shamir_reconstruct(&shares[0..3], 97);
        assert_eq!(reconstructed, secret);
        // Different subset of 3 should also work
        let reconstructed2 = shamir_reconstruct(&shares[2..5], 97);
        assert_eq!(reconstructed2, secret);
    }

    #[test]
    #[ignore]
    fn test_shamir_insufficient_shares() {
        let secret = 42_u64;
        let shares = shamir_share(secret, 3, 5, 97);
        // Only 2 shares should NOT reconstruct correctly (with high probability)
        let wrong = shamir_reconstruct(&shares[0..2], 97);
        // We can't assert != because there's a small chance it's correct,
        // but for t=3 it almost certainly won't be.
        let _ = wrong; // Just verify it doesn't panic
    }

    #[test]
    #[ignore]
    fn test_additive_roundtrip() {
        let secret = 12345_u64;
        let shares = additive_share(secret, 5);
        assert_eq!(shares.len(), 5);
        let reconstructed = additive_reconstruct(&shares);
        assert_eq!(reconstructed, secret);
    }
}
