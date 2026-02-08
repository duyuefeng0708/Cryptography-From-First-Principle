/// Display a value in binary with a given bit width.
pub fn to_binary_string(val: u64, width: usize) -> String {
    format!("{:0>width$b}", val, width = width)
}

/// Simple assertion helper with descriptive message for exercises.
pub fn check(condition: bool, msg: &str) {
    assert!(condition, "Exercise check failed: {}", msg);
}
