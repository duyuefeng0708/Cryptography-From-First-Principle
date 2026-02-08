//! # Module 03: Galois Fields and AES — Exercises
//!
//! All GF(256) arithmetic uses the AES irreducible polynomial:
//! `x⁸ + x⁴ + x³ + x + 1` (0x11B in hex).
//!
//! ## Progression
//! 1. `gf256_add`      — Guided (it's XOR)
//! 2. `gf256_mul`      — Scaffolded (Russian peasant + reduction)
//! 3. `gf256_inv`      — Scaffolded (hint: use extended Euclidean or Fermat)
//! 4. `aes_sbox`       — Scaffolded (compose inverse + affine)
//! 5. `aes_mix_column` — Independent

/// The AES irreducible polynomial: x⁸ + x⁴ + x³ + x + 1.
const AES_POLY: u16 = 0x11B;

/// Add two elements in GF(256). This is just XOR.
///
/// # Example
/// ```
/// # use galois_fields_aes::gf256_add;
/// assert_eq!(gf256_add(0x57, 0x83), 0xD4);
/// ```
pub fn gf256_add(a: u8, b: u8) -> u8 {
    // In GF(2^n), addition is XOR. That's it!
    todo!("XOR a and b")
}

/// Multiply two elements in GF(256) using the AES irreducible polynomial.
///
/// Use the "Russian peasant" (shift-and-XOR) algorithm:
/// - Shift `a` left by 1 bit each iteration (multiply by x)
/// - If the shift overflows 8 bits, reduce by XORing with AES_POLY
/// - If the corresponding bit of `b` is set, XOR `a` into the result
pub fn gf256_mul(a: u8, b: u8) -> u8 {
    // Hint: work with u16 to catch overflow past 8 bits.
    // For each bit of b (from bit 0 to bit 7):
    //   if bit is set, result ^= a
    //   shift a left by 1
    //   if a overflows 8 bits (bit 8 set), reduce: a ^= AES_POLY
    todo!("GF(256) multiplication with polynomial reduction")
}

/// Compute the multiplicative inverse of `a` in GF(256).
///
/// Returns 0 if `a == 0` (by convention for AES S-box).
///
/// Hint: By Fermat's little theorem in GF(2^8), a^(254) = a^(-1).
/// Alternatively, implement the extended Euclidean algorithm for polynomials.
pub fn gf256_inv(a: u8) -> u8 {
    todo!("Multiplicative inverse in GF(256)")
}

/// Compute the AES S-box value for a single byte.
///
/// S-box(a) = affine_transform(gf256_inv(a))
///
/// The affine transform over GF(2) is:
///   b[i] = inv[i] ^ inv[(i+4)%8] ^ inv[(i+5)%8] ^ inv[(i+6)%8] ^ inv[(i+7)%8] ^ c[i]
/// where c = 0x63.
pub fn aes_sbox(byte: u8) -> u8 {
    todo!("AES S-box: inverse then affine transform")
}

/// Apply the AES MixColumns transformation to a single column.
///
/// Multiplies the column vector by the fixed matrix in GF(256):
/// ```text
/// | 2 3 1 1 |   | c0 |
/// | 1 2 3 1 | × | c1 |
/// | 1 1 2 3 |   | c2 |
/// | 3 1 1 2 |   | c3 |
/// ```
pub fn aes_mix_column(col: [u8; 4]) -> [u8; 4] {
    todo!("MixColumns matrix multiplication in GF(256)")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn test_gf256_add() {
        assert_eq!(gf256_add(0x57, 0x83), 0xD4);
        assert_eq!(gf256_add(0xFF, 0xFF), 0x00); // self-inverse
    }

    #[test]
    #[ignore]
    fn test_gf256_mul_basic() {
        assert_eq!(gf256_mul(0x57, 0x83), 0xC1);
    }

    #[test]
    #[ignore]
    fn test_gf256_mul_identity() {
        assert_eq!(gf256_mul(0x53, 0x01), 0x53); // multiply by 1
        assert_eq!(gf256_mul(0x00, 0x53), 0x00); // multiply by 0
    }

    #[test]
    #[ignore]
    fn test_gf256_inv() {
        // inv(0x53) × 0x53 should equal 1
        let inv = gf256_inv(0x53);
        assert_eq!(gf256_mul(inv, 0x53), 0x01);
        assert_eq!(gf256_inv(0x00), 0x00); // special case
    }

    #[test]
    #[ignore]
    fn test_aes_sbox_known_values() {
        assert_eq!(aes_sbox(0x00), 0x63);
        assert_eq!(aes_sbox(0x01), 0x7C);
        assert_eq!(aes_sbox(0x53), 0xED);
    }

    #[test]
    #[ignore]
    fn test_aes_mix_column() {
        // FIPS 197 test vector
        let input = [0xDB, 0x13, 0x53, 0x45];
        let expected = [0x8E, 0x4D, 0xA1, 0xBC];
        assert_eq!(aes_mix_column(input), expected);
    }
}
