//! Integration tests for the starter library: fail-fast configuration and
//! the example service contract, exercised through the public API.

use starter::config::Config;
use starter::greeter;
use starter::logging::LogSeverity;

#[test]
fn config_requires_service_name() {
    std::env::remove_var("SERVICE_NAME");
    let error = Config::from_environment().expect_err("must fail without SERVICE_NAME");
    assert!(error.0.contains("SERVICE_NAME"));
}

#[test]
fn config_defaults_log_level_to_information() {
    std::env::set_var("SERVICE_NAME", "demo");
    std::env::remove_var("APP_LOG_LEVEL");

    let config = Config::from_environment().expect("valid config");
    assert_eq!(config.service_name, "demo");
    assert_eq!(config.log_level, LogSeverity::Information);
}

#[test]
fn config_rejects_unknown_log_level() {
    std::env::set_var("SERVICE_NAME", "demo");
    std::env::set_var("APP_LOG_LEVEL", "loud");

    let error = Config::from_environment().expect_err("must fail on unknown level");
    assert!(error.0.contains("APP_LOG_LEVEL"));

    std::env::remove_var("APP_LOG_LEVEL");
}

#[test]
fn greeter_validates_and_greets() {
    assert_eq!(greeter::greet("ForgeBase"), Ok("Hello, ForgeBase!".into()));
    assert!(greeter::greet("  ").is_err());
}
