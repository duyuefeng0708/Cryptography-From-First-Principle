//! # Module 08: Lattices and Post-Quantum Cryptography — Exercises
//!
//! ## Progression
//! 1. `gram_schmidt_2d` — signature + doc
//! 2. `lll_reduce_2d`   — signature + doc
//! 3. `lwe_keygen`      — signature + doc
//! 4. `lwe_encrypt`     — signature + doc
//! 5. `lwe_decrypt`     — signature only

/// Compute the Gram-Schmidt orthogonalization of two 2D basis vectors.
///
/// Given basis vectors b1 and b2, compute the orthogonal basis b1*, b2*
/// where b2* = b2 - proj(b2, b1*).
///
/// Returns the orthogonalized basis as f64 vectors.
pub fn gram_schmidt_2d(b1: [i64; 2], b2: [i64; 2]) -> ([f64; 2], [f64; 2]) {
    todo!("2D Gram-Schmidt orthogonalization")
}

/// Apply the LLL algorithm to a 2D lattice basis.
///
/// The LLL algorithm produces a "reduced" basis where the vectors are
/// nearly orthogonal and short. For 2D, this is equivalent to the
/// Gaussian lattice reduction algorithm.
///
/// Returns the reduced basis vectors.
pub fn lll_reduce_2d(b1: [i64; 2], b2: [i64; 2]) -> ([i64; 2], [i64; 2]) {
    todo!("2D LLL (Gaussian) lattice reduction")
}

/// Generate an LWE key pair.
///
/// - Choose a random secret vector `s` of dimension `n` (mod `q`)
/// - Generate a random matrix `A` of size `m × n` (mod `q`)
/// - Compute `b = A*s + e` where `e` is a small noise vector
///
/// Returns `(A, b, s)` — public key is `(A, b)`, secret key is `s`.
pub fn lwe_keygen(n: usize, m: usize, q: i64) -> (Vec<Vec<i64>>, Vec<i64>, Vec<i64>) {
    todo!("LWE key generation: A, b = As + e, s")
}

/// Encrypt a single bit using LWE.
///
/// To encrypt bit `msg` ∈ {0, 1}:
/// - Choose a random subset S of the rows of A
/// - Compute `u = Σ A[i] for i in S` (mod q)
/// - Compute `v = Σ b[i] for i in S + msg * ⌊q/2⌋` (mod q)
///
/// Returns ciphertext `(u, v)`.
pub fn lwe_encrypt(a: &[Vec<i64>], b: &[i64], msg: u8, q: i64) -> (Vec<i64>, i64) {
    todo!("LWE encryption of a single bit")
}

/// Decrypt an LWE ciphertext.
///
/// Compute `v - <u, s>` mod q. If the result is closer to 0, the bit is 0.
/// If closer to q/2, the bit is 1.
pub fn lwe_decrypt(s: &[i64], u: &[i64], v: i64, q: i64) -> u8 {
    todo!("LWE decryption: recover bit from noisy inner product")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_gram_schmidt_2d() {
        let (b1s, b2s) = gram_schmidt_2d([3, 1], [2, 2]);
        // b1* should be unchanged
        assert!((b1s[0] - 3.0).abs() < 1e-10);
        assert!((b1s[1] - 1.0).abs() < 1e-10);
        // b2* should be orthogonal to b1*
        let dot = b1s[0] * b2s[0] + b1s[1] * b2s[1];
        assert!(dot.abs() < 1e-10, "Should be orthogonal");
    }

    #[test]
    #[ignore]
    fn test_lll_reduce_2d() {
        // A bad basis for the same lattice
        let (r1, r2) = lll_reduce_2d([1, 0], [100, 1]);
        // Reduced basis should have shorter vectors
        let norm_sq = |v: [i64; 2]| (v[0] * v[0] + v[1] * v[1]) as f64;
        assert!(norm_sq(r1) <= norm_sq([100, 1]) as f64);
        assert!(norm_sq(r2) <= norm_sq([100, 1]) as f64);
    }

    #[test]
    #[ignore]
    fn test_lwe_roundtrip() {
        let q = 97;
        let (a, b, s) = lwe_keygen(4, 8, q);
        for msg in [0u8, 1u8] {
            let (u, v) = lwe_encrypt(&a, &b, msg, q);
            let decrypted = lwe_decrypt(&s, &u, v, q);
            assert_eq!(decrypted, msg, "LWE decrypt should recover the bit");
        }
    }
}
