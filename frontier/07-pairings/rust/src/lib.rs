//! # Module 07: Bilinear Pairings — Exercises
//!
//! Pairings are hard to implement from scratch in toy code.
//! These exercises focus on using pairing-like abstractions for BLS signatures.
//!
//! ## Progression
//! 1. `bls_sign`             — signature + doc
//! 2. `bls_verify`           — signature + doc
//! 3. `bls_aggregate_sigs`   — signature + doc
//! 4. `bls_aggregate_verify` — signature only

/// Placeholder type for a group element (in a real implementation, this
/// would be a point on a pairing-friendly curve).
pub type GroupElement = u64;

/// Placeholder pairing function type: e(G1, G2) -> GT.
pub type PairingFn = fn(GroupElement, GroupElement) -> GroupElement;

/// Sign a message point with a secret key: σ = sk * H(m).
///
/// In BLS, the signature is a scalar multiplication of the
/// hash-to-curve output by the secret key.
pub fn bls_sign(sk: u64, message_point: GroupElement) -> GroupElement {
    todo!("BLS sign: sk * H(m)")
}

/// Verify a BLS signature.
///
/// Check that e(σ, g2) == e(H(m), pk) where:
/// - σ is the signature
/// - g2 is the generator of G2
/// - H(m) is the message hashed to G1
/// - pk is the public key in G2
pub fn bls_verify(
    sig: GroupElement,
    g2: GroupElement,
    message_point: GroupElement,
    pk: GroupElement,
    pairing: PairingFn,
) -> bool {
    todo!("BLS verify: check pairing equation")
}

/// Aggregate multiple BLS signatures into one.
///
/// Aggregation is simply the sum (or product, depending on group notation)
/// of all individual signatures.
pub fn bls_aggregate_sigs(sigs: &[GroupElement]) -> GroupElement {
    todo!("Sum/combine all signatures into one")
}

/// Verify an aggregated BLS signature against multiple public keys and messages.
///
/// For distinct-message aggregation:
/// e(σ_agg, g2) == ∏ e(H(m_i), pk_i)
pub fn bls_aggregate_verify(
    agg_sig: GroupElement,
    g2: GroupElement,
    message_points: &[GroupElement],
    pks: &[GroupElement],
    pairing: PairingFn,
) -> bool {
    todo!("Verify aggregated BLS signature")
}

#[cfg(test)]
mod tests {
    use super::*;

    // Toy "pairing": simple multiplication (NOT cryptographically meaningful).
    fn toy_pairing(a: GroupElement, b: GroupElement) -> GroupElement {
        a.wrapping_mul(b)
    }

    #[test]
    #[ignore]
    fn test_bls_sign() {
        let sig = bls_sign(42, 7);
        assert_ne!(sig, 0);
    }

    #[test]
    #[ignore]
    fn test_bls_aggregate_sigs() {
        let sigs = vec![10, 20, 30];
        let agg = bls_aggregate_sigs(&sigs);
        assert_ne!(agg, 0);
    }
}
