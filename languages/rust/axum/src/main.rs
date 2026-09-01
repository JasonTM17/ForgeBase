//! Fail fast before binding: a broken deployment configuration must never
//! turn into runtime request failures.

use axum_starter::api::{self, AppState};
use axum_starter::config::Config;
use axum_starter::logging::{self, LogSeverity};
use axum_starter::shutdown::shutdown_signal;

#[tokio::main]
async fn main() {
    let config = match Config::from_environment() {
        Ok(config) => config,
        Err(error) => {
            eprintln!("configuration error: {error}");
            std::process::exit(2);
        }
    };

    logging::log(
        config.log_level,
        LogSeverity::Information,
        &config.service_name,
        "service starting",
    );

    let app = api::router(AppState);
    let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{}", config.port))
        .await
        .expect("bind listener");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .expect("server run");

    logging::log(
        config.log_level,
        LogSeverity::Information,
        &config.service_name,
        "service stopped",
    );
}
