//! Example domain service. It exists to demonstrate the shape a real
//! service takes (validation -> behavior), not to carry business meaning —
//! replace it when copying the template out.

#[derive(Debug, PartialEq, Eq)]
pub struct EmptyName;

pub fn greet(name: &str) -> Result<String, EmptyName> {
    if name.trim().is_empty() {
        return Err(EmptyName);
    }
    Ok(format!("Hello, {name}!"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greets_by_name() {
        assert_eq!(greet("ForgeBase"), Ok("Hello, ForgeBase!".to_string()));
    }

    #[test]
    fn rejects_whitespace_only_names() {
        assert_eq!(greet("   "), Err(EmptyName));
    }
}
