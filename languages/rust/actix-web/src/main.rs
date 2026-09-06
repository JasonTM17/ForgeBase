//! Fail fast before binding: a broken deployment configuration must never
//! turn into runtime request failures.

use actix_starter::api::WidgetStore;
use actix_starter::config::Config;
use actix_starter::logging::{self, LogSeverity};
use actix_web::middleware::Logger;
use actix_web::{web, App, HttpServer};

#[tokio::main]
async fn main() -> std::io::Result<()> {
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

    // actix Logger uses env_logger-style output; initialize with the
    // configured level so request logs honor APP_LOG_LEVEL. RUST_LOG remains
    // an explicit operator override when it is set.
    let default_filter = match config.log_level {
        LogSeverity::Critical | LogSeverity::Error => "error",
        LogSeverity::Warning => "warn",
        LogSeverity::Information => "info",
        LogSeverity::Debug => "debug",
        LogSeverity::Trace => "trace",
    };
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or(default_filter))
        .init();

    // One shared store across all workers (Data is an Arc under the hood).
    let store = web::Data::new(WidgetStore::default());

    let bind = format!("0.0.0.0:{}", config.port);
    HttpServer::new(move || {
        App::new()
            .app_data(store.clone())
            .wrap(Logger::default())
            .configure(actix_starter::api::configure)
    })
    .bind(bind)?
    .run()
    .await
}
