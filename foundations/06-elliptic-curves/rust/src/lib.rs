//! # Module 06: Elliptic Curves — Exercises
//!
//! All curves are in short Weierstrass form: y² = x³ + ax + b over GF(p).
//!
//! ## Progression
//! 1. `point_add`          — Scaffolded (formulas in doc)
//! 2. `point_double`       — Scaffolded (tangent formula)
//! 3. `scalar_mul`         — Independent (double-and-add)
//! 4. `ecdh_shared_secret` — Independent
//! 5. `ecdsa_verify`       — Independent

/// A point on an elliptic curve, or the point at infinity.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Point {
    /// The identity element (point at infinity).
    Infinity,
    /// An affine point (x, y).
    Affine(i64, i64),
}

/// Curve parameters: y² = x³ + ax + b (mod p).
#[derive(Debug, Clone, Copy)]
pub struct CurveParams {
    pub a: i64,
    pub b: i64,
    pub p: i64,
}

/// Add two points on the curve.
///
/// Formulas (when P ≠ Q, neither is infinity):
///   λ = (y₂ - y₁) / (x₂ - x₁) mod p
///   x₃ = λ² - x₁ - x₂ mod p
///   y₃ = λ(x₁ - x₃) - y₁ mod p
///
/// Handle special cases: infinity, same point (use `point_double`),
/// vertical line (x₁ = x₂, y₁ = -y₂ → Infinity).
pub fn point_add(p1: Point, p2: Point, curve: &CurveParams) -> Point {
    todo!("Elliptic curve point addition")
}

/// Double a point on the curve.
///
/// Formula (when P is not infinity and y ≠ 0):
///   λ = (3x² + a) / (2y) mod p
///   x₃ = λ² - 2x mod p
///   y₃ = λ(x - x₃) - y mod p
pub fn point_double(p: Point, curve: &CurveParams) -> Point {
    todo!("Elliptic curve point doubling")
}

/// Scalar multiplication: compute `k * P` using double-and-add.
pub fn scalar_mul(k: u64, p: Point, curve: &CurveParams) -> Point {
    todo!("Double-and-add scalar multiplication")
}

/// Compute ECDH shared secret: `sk * other_public_key`.
pub fn ecdh_shared_secret(sk: u64, pk: Point, curve: &CurveParams) -> Point {
    todo!("ECDH: scalar_mul(sk, pk)")
}

/// Verify an ECDSA signature.
///
/// Given message hash `z`, signature `(r, s)`, public key `pk`,
/// generator `g` with order `n`:
///   w  = s^(-1) mod n
///   u1 = z * w mod n
///   u2 = r * w mod n
///   R  = u1*G + u2*pk
///   valid iff R.x ≡ r (mod n)
pub fn ecdsa_verify(
    z: u64,
    r: u64,
    s: u64,
    pk: Point,
    g: Point,
    n: u64,
    curve: &CurveParams,
) -> bool {
    todo!("ECDSA signature verification")
}

/// Helper: compute modular inverse using Fermat's little theorem.
/// Only works when `p` is prime: a^(-1) = a^(p-2) mod p.
fn mod_inv(a: i64, p: i64) -> i64 {
    mod_pow(a.rem_euclid(p), (p - 2) as u64, p)
}

/// Helper: modular exponentiation for i64 values.
fn mod_pow(mut base: i64, mut exp: u64, modulus: i64) -> i64 {
    let mut result = 1i64;
    base = base.rem_euclid(modulus);
    while exp > 0 {
        if exp % 2 == 1 {
            result = (result as i128 * base as i128).rem_euclid(modulus as i128) as i64;
        }
        exp /= 2;
        base = (base as i128 * base as i128).rem_euclid(modulus as i128) as i64;
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    fn test_curve() -> CurveParams {
        // y² = x³ + 2x + 3 over GF(97)
        CurveParams { a: 2, b: 3, p: 97 }
    }

    #[test]
    #[ignore]
    fn test_point_add_basic() {
        let c = test_curve();
        let p1 = Point::Affine(3, 6);
        let p2 = Point::Affine(80, 10);
        let sum = point_add(p1, p2, &c);
        // Verify the result is on the curve
        if let Point::Affine(x, y) = sum {
            let lhs = (y * y).rem_euclid(c.p);
            let rhs = (x * x * x + c.a * x + c.b).rem_euclid(c.p);
            assert_eq!(lhs, rhs, "Result should be on the curve");
        }
    }

    #[test]
    #[ignore]
    fn test_point_add_infinity() {
        let c = test_curve();
        let p1 = Point::Affine(3, 6);
        assert_eq!(point_add(p1, Point::Infinity, &c), p1);
        assert_eq!(point_add(Point::Infinity, p1, &c), p1);
    }

    #[test]
    #[ignore]
    fn test_point_double() {
        let c = test_curve();
        let p1 = Point::Affine(3, 6);
        let doubled = point_double(p1, &c);
        if let Point::Affine(x, y) = doubled {
            let lhs = (y * y).rem_euclid(c.p);
            let rhs = (x * x * x + c.a * x + c.b).rem_euclid(c.p);
            assert_eq!(lhs, rhs, "Doubled point should be on the curve");
        }
    }

    #[test]
    #[ignore]
    fn test_scalar_mul_identity() {
        let c = test_curve();
        let p1 = Point::Affine(3, 6);
        assert_eq!(scalar_mul(1, p1, &c), p1);
    }

    #[test]
    #[ignore]
    fn test_ecdh() {
        let c = test_curve();
        let g = Point::Affine(3, 6);
        let (a, b) = (7_u64, 11_u64);
        let pk_a = scalar_mul(a, g, &c);
        let pk_b = scalar_mul(b, g, &c);
        let shared_a = ecdh_shared_secret(a, pk_b, &c);
        let shared_b = ecdh_shared_secret(b, pk_a, &c);
        assert_eq!(shared_a, shared_b, "Both parties should derive same shared secret");
    }
}
