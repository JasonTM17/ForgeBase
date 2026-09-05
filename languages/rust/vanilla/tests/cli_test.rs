//! Integration tests for the starter library: fail-fast configuration and
//! the example service contract, exercised through the public API.

use starter::config::Config;
use starter::greeter;
use starter::logging::LogSeverity;
use std::sync::{Mutex, MutexGuard, OnceLock};

static ENV_LOCK: OnceLock<Mutex<()>> = OnceLock::new();

fn env_lock() -> MutexGuard<'static, ()> {
    ENV_LOCK
        .get_or_init(|| Mutex::new(()))
        .lock()
        .unwrap_or_else(|poisoned| poisoned.into_inner())
}

struct EnvSnapshot {
    values: Vec<(&'static str, Option<String>)>,
}

impl EnvSnapshot {
    fn capture(names: &[&'static str]) -> Self {
        Self {
            values: names
                .iter()
                .map(|name| (*name, std::env::var(name).ok()))
                .collect(),
        }
    }
}

impl Drop for EnvSnapshot {
    fn drop(&mut self) {
        for (name, value) in &self.values {
            match value {
                Some(value) => std::env::set_var(name, value),
                None => std::env::remove_var(name),
            }
        }
    }
}

#[test]
fn config_requires_service_name() {
    let _lock = env_lock();
    let _snapshot = EnvSnapshot::capture(&["SERVICE_NAME", "APP_LOG_LEVEL"]);
    std::env::remove_var("SERVICE_NAME");
    let error = Config::from_environment().expect_err("must fail without SERVICE_NAME");
    assert!(error.0.contains("SERVICE_NAME"));
}

#[test]
fn config_defaults_log_level_to_information() {
    let _lock = env_lock();
    let _snapshot = EnvSnapshot::capture(&["SERVICE_NAME", "APP_LOG_LEVEL"]);
    std::env::set_var("SERVICE_NAME", "demo");
    std::env::remove_var("APP_LOG_LEVEL");

    let config = Config::from_environment().expect("valid config");
    assert_eq!(config.service_name, "demo");
    assert_eq!(config.log_level, LogSeverity::Information);
}

#[test]
fn config_rejects_unknown_log_level() {
    let _lock = env_lock();
    let _snapshot = EnvSnapshot::capture(&["SERVICE_NAME", "APP_LOG_LEVEL"]);
    std::env::set_var("SERVICE_NAME", "demo");
    std::env::set_var("APP_LOG_LEVEL", "loud");

    let error = Config::from_environment().expect_err("must fail on unknown level");
    assert!(error.0.contains("APP_LOG_LEVEL"));
}

#[test]
fn greeter_validates_and_greets() {
    assert_eq!(greeter::greet("ForgeBase"), Ok("Hello, ForgeBase!".into()));
    assert!(greeter::greet("  ").is_err());
}
