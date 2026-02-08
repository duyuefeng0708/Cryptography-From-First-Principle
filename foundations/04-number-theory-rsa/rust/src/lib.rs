//! # Module 04: Number Theory and RSA — Exercises
//!
//! ## Progression
//! 1. `extended_gcd`        — Guided (recursive skeleton)
//! 2. `mod_inverse`         — Scaffolded (use extended_gcd)
//! 3. `euler_totient`       — Scaffolded (factorization hint)
//! 4. `rsa_keygen`          — Scaffolded (from given primes)
//! 5. `rsa_encrypt_decrypt` — Independent

/// Compute the extended GCD: returns (gcd, x, y) such that a*x + b*y = gcd.
///
/// # Example
/// ```
/// # use number_theory_rsa::extended_gcd;
/// let (g, x, y) = extended_gcd(35, 15);
/// assert_eq!(g, 5);
/// assert_eq!(35_i64 * x + 15_i64 * y, 5);
/// ```
pub fn extended_gcd(a: i64, b: i64) -> (i64, i64, i64) {
    // Base case: if b == 0, return (a, 1, 0).
    // Recursive case:
    //   let (g, x1, y1) = extended_gcd(b, a % b);
    //   return (g, y1, x1 - (a / b) * y1);
    //
    // TODO: implement the recursion (or convert to iterative).
    if b == 0 {
        return (a, 1, 0);
    }
    todo!("Recursive step of extended GCD")
}

/// Compute the modular inverse of `a` mod `m`, if it exists.
///
/// Returns `Some(x)` where `a * x ≡ 1 (mod m)`, or `None` if gcd(a,m) != 1.
///
/// Hint: use `extended_gcd`. If gcd == 1, the inverse is `x mod m`.
pub fn mod_inverse(a: u64, m: u64) -> Option<u64> {
    todo!("Use extended_gcd to find modular inverse")
}

/// Compute Euler's totient φ(n).
///
/// φ(n) = n × ∏(1 - 1/p) for each distinct prime factor p of n.
///
/// For RSA: if n = p*q, then φ(n) = (p-1)(q-1).
///
/// Hint: factor n by trial division up to √n.
pub fn euler_totient(n: u64) -> u64 {
    todo!("Compute Euler's totient via trial division")
}

/// Generate RSA key components from two primes p and q.
///
/// Returns `(n, e, d)` where:
/// - `n = p * q`
/// - `e = 65537` (standard public exponent)
/// - `d = e^(-1) mod φ(n)`
///
/// Panics if e and φ(n) are not coprime.
pub fn rsa_keygen(p: u64, q: u64) -> (u64, u64, u64) {
    todo!("Compute n, e=65537, d from primes p and q")
}

/// RSA encryption or decryption: compute `msg^key mod n`.
///
/// This works for both encryption (msg^e mod n) and decryption (ciphertext^d mod n).
pub fn rsa_encrypt_decrypt(msg: u64, key: u64, n: u64) -> u64 {
    todo!("Modular exponentiation for RSA")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_extended_gcd_basic() {
        let (g, x, y) = extended_gcd(35, 15);
        assert_eq!(g, 5);
        assert_eq!(35 * x + 15 * y, 5);
    }

    #[test]
    #[ignore]
    fn test_extended_gcd_coprime() {
        let (g, x, y) = extended_gcd(17, 13);
        assert_eq!(g, 1);
        assert_eq!(17 * x + 13 * y, 1);
    }

    #[test]
    #[ignore]
    fn test_mod_inverse_exists() {
        assert_eq!(mod_inverse(3, 7), Some(5)); // 3*5 = 15 ≡ 1 mod 7
    }

    #[test]
    #[ignore]
    fn test_mod_inverse_none() {
        assert_eq!(mod_inverse(6, 9), None); // gcd(6,9) = 3
    }

    #[test]
    #[ignore]
    fn test_euler_totient() {
        assert_eq!(euler_totient(7), 6);   // prime
        assert_eq!(euler_totient(12), 4);  // 12 = 2²×3, φ = 12(1-1/2)(1-1/3) = 4
        assert_eq!(euler_totient(15), 8);  // 15 = 3×5, φ = (3-1)(5-1) = 8
    }

    #[test]
    #[ignore]
    fn test_rsa_roundtrip() {
        let (n, e, d) = rsa_keygen(61, 53);
        assert_eq!(n, 3233);

        let plaintext = 42_u64;
        let ciphertext = rsa_encrypt_decrypt(plaintext, e, n);
        let decrypted = rsa_encrypt_decrypt(ciphertext, d, n);
        assert_eq!(decrypted, plaintext);
    }
}
