//! # Module 11: Homomorphic Encryption — Exercises
//!
//! We implement Paillier (additive HE) as a concrete, tractable scheme.
//!
//! ## Progression
//! 1. `paillier_keygen`      — signature + doc
//! 2. `paillier_encrypt`     — signature + doc
//! 3. `paillier_add`         — signature + doc
//! 4. `paillier_decrypt`     — signature only
//! 5. `paillier_scalar_mul`  — signature only

/// Paillier public key: (n, g) where n = p*q.
#[derive(Debug, Clone)]
pub struct PaillierPk {
    pub n: u128,
    pub g: u128,
    pub n_sq: u128,
}

/// Paillier secret key: (lambda, mu).
#[derive(Debug, Clone)]
pub struct PaillierSk {
    pub lambda: u128,
    pub mu: u128,
    pub n: u128,
    pub n_sq: u128,
}

/// Generate Paillier keys from two primes p and q.
///
/// - n = p * q
/// - λ = lcm(p-1, q-1)
/// - g = n + 1 (simple choice)
/// - μ = L(g^λ mod n²)^(-1) mod n, where L(x) = (x-1)/n
pub fn paillier_keygen(p: u128, q: u128) -> (PaillierPk, PaillierSk) {
    todo!("Paillier key generation")
}

/// Encrypt a plaintext m ∈ [0, n) using Paillier.
///
/// c = g^m * r^n mod n²
/// where r is a random value coprime to n.
pub fn paillier_encrypt(pk: &PaillierPk, m: u128, r: u128) -> u128 {
    todo!("Paillier encryption: g^m * r^n mod n^2")
}

/// Homomorphic addition: add two ciphertexts.
///
/// Enc(m1) * Enc(m2) mod n² = Enc(m1 + m2 mod n)
pub fn paillier_add(pk: &PaillierPk, c1: u128, c2: u128) -> u128 {
    todo!("Multiply ciphertexts for additive homomorphism")
}

/// Decrypt a Paillier ciphertext.
///
/// m = L(c^λ mod n²) * μ mod n
pub fn paillier_decrypt(sk: &PaillierSk, c: u128) -> u128 {
    todo!("Paillier decryption")
}

/// Homomorphic scalar multiplication: multiply plaintext by a constant.
///
/// c^scalar mod n² = Enc(m * scalar mod n)
pub fn paillier_scalar_mul(pk: &PaillierPk, c: u128, scalar: u128) -> u128 {
    todo!("Exponentiate ciphertext for scalar multiplication")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_paillier_roundtrip() {
        let (pk, sk) = paillier_keygen(13, 17);
        let m = 42_u128;
        let r = 77_u128; // random, coprime to n
        let c = paillier_encrypt(&pk, m, r);
        let decrypted = paillier_decrypt(&sk, c);
        assert_eq!(decrypted, m);
    }

    #[test]
    #[ignore]
    fn test_paillier_additive_homomorphism() {
        let (pk, sk) = paillier_keygen(13, 17);
        let m1 = 20_u128;
        let m2 = 30_u128;
        let c1 = paillier_encrypt(&pk, m1, 53);
        let c2 = paillier_encrypt(&pk, m2, 79);
        let c_sum = paillier_add(&pk, c1, c2);
        let decrypted = paillier_decrypt(&sk, c_sum);
        assert_eq!(decrypted, (m1 + m2) % pk.n);
    }
}
