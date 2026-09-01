//! Fail-fast configuration: missing required variables or values that fail
//! validation abort startup before any real work happens, so
//! misconfiguration is never discovered in production traffic.

use crate::logging::LogSeverity;
use std::env;

#[derive(Debug, Clone)]
pub struct Config {
    pub service_name: String,
    pub log_level: LogSeverity,
}

/// Raised only for configuration problems; the binary maps it to a clean
/// exit message instead of a stack trace.
#[derive(Debug)]
pub struct ConfigError(pub String);

impl std::fmt::Display for ConfigError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for ConfigError {}

impl Config {
    /// Reads the process environment.
    pub fn from_environment() -> Result<Self, ConfigError> {
        let service_name = required("SERVICE_NAME")?;
        let level_name = optional("APP_LOG_LEVEL", "information");
        let log_level = LogSeverity::parse(&level_name).ok_or_else(|| {
            ConfigError(format!(
                "APP_LOG_LEVEL '{level_name}' is invalid. Valid values: \
                 critical, error, warning, information, debug, trace."
            ))
        })?;
        Ok(Self {
            service_name,
            log_level,
        })
    }
}

fn required(name: &str) -> Result<String, ConfigError> {
    match env::var(name) {
        Ok(value) if !value.trim().is_empty() => Ok(value),
        _ => Err(ConfigError(format!(
            "required environment variable {name} is missing or empty"
        ))),
    }
}

fn optional(name: &str, fallback: &str) -> String {
    match env::var(name) {
        Ok(value) if !value.trim().is_empty() => value,
        _ => fallback.to_string(),
    }
}
