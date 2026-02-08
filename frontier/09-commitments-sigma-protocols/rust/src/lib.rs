//! # Module 09: Commitment Schemes and Sigma Protocols — Exercises
//!
//! ## Progression
//! 1. `pedersen_commit`  — signature + doc
//! 2. `pedersen_verify`  — signature + doc
//! 3. `schnorr_prove`    — signature + doc
//! 4. `schnorr_verify`   — signature + doc
//! 5. `fiat_shamir`      — signature only

/// Create a Pedersen commitment: C = g^m * h^r mod p.
///
/// - `g`, `h`: generators (h must have unknown discrete log w.r.t. g)
/// - `m`: the message/value to commit to
/// - `r`: randomness (blinding factor)
/// - `p`: prime modulus
pub fn pedersen_commit(g: u64, h: u64, m: u64, r: u64, p: u64) -> u64 {
    todo!("C = g^m * h^r mod p")
}

/// Verify a Pedersen commitment opening.
///
/// Check that `commitment == g^m * h^r mod p`.
pub fn pedersen_verify(g: u64, h: u64, m: u64, r: u64, commitment: u64, p: u64) -> bool {
    todo!("Check commitment == g^m * h^r mod p")
}

/// Generate a Schnorr proof of knowledge of discrete log.
///
/// Prover knows `x` such that `pk = g^x mod p`.
/// Protocol:
///   1. Choose random `k`, compute `commitment = g^k mod p`
///   2. Receive `challenge` (from verifier or Fiat-Shamir)
///   3. Compute `response = k - x * challenge mod (p-1)`
///
/// Returns `(commitment, challenge, response)`.
pub fn schnorr_prove(
    g: u64,
    x: u64,
    p: u64,
    k: u64,
    challenge: u64,
) -> (u64, u64, u64) {
    todo!("Schnorr proof: (g^k, challenge, k - x*challenge mod p-1)")
}

/// Verify a Schnorr proof.
///
/// Check: g^response * pk^challenge ≡ commitment (mod p).
pub fn schnorr_verify(
    g: u64,
    pk: u64,
    commitment: u64,
    challenge: u64,
    response: u64,
    p: u64,
) -> bool {
    todo!("Check g^response * pk^challenge == commitment mod p")
}

/// Apply the Fiat-Shamir transform: derive challenge from transcript.
///
/// Hash the concatenation of (g, pk, commitment, message) to produce
/// a deterministic challenge. Use a simple hash for this exercise.
///
/// Returns the challenge value.
pub fn fiat_shamir(g: u64, pk: u64, commitment: u64, message: &[u8]) -> u64 {
    todo!("Hash-based challenge derivation")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_pedersen_commit_verify() {
        let p = 23;
        let g = 4;
        let h = 9;
        let m = 5;
        let r = 3;
        let c = pedersen_commit(g, h, m, r, p);
        assert!(pedersen_verify(g, h, m, r, c, p));
        // Wrong message should fail
        assert!(!pedersen_verify(g, h, m + 1, r, c, p));
    }

    #[test]
    #[ignore]
    fn test_schnorr_roundtrip() {
        let p = 23;
        let g = 5;
        let x = 7; // secret key
        // pk = g^x mod p
        let pk = 5_u64.pow(7) % 23; // = 17
        let k = 3; // random nonce
        let challenge = 11;
        let (comm, ch, resp) = schnorr_prove(g, x, p, k, challenge);
        assert_eq!(ch, challenge);
        assert!(schnorr_verify(g, pk, comm, ch, resp, p));
    }
}
