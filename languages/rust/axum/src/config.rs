//! Fail-fast configuration: the API refuses to start on missing or invalid
//! settings so misconfiguration is never discovered through request
//! traffic.

use std::env;

use crate::logging::LogSeverity;

#[derive(Debug, Clone)]
pub struct Config {
    pub service_name: String,
    pub log_level: LogSeverity,
    pub port: u16,
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
    pub fn from_environment() -> Result<Self, ConfigError> {
        let service_name = required("SERVICE_NAME")?;
        let level_name = optional("APP_LOG_LEVEL", "information");
        let log_level = LogSeverity::parse(&level_name).ok_or_else(|| {
            ConfigError(format!(
                "APP_LOG_LEVEL '{level_name}' is invalid. Valid values: \
                 critical, error, warning, information, debug, trace."
            ))
        })?;
        let port_raw = optional("PORT", "8080");
        let port: u16 = port_raw.parse().map_err(|_| {
            ConfigError(format!(
                "PORT '{port_raw}' is invalid. Expected an integer in 1..65535."
            ))
        })?;
        Ok(Self {
            service_name,
            log_level,
            port,
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
