//! Fail-fast demo: a missing or invalid configuration variable exits with a
//! clean message and a non-zero code instead of a stack trace.

use starter::config::Config;
use starter::greeter;
use starter::logging::{self, LogSeverity};

fn main() {
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
    match greeter::greet("ForgeBase") {
        Ok(greeting) => println!("{greeting}"),
        Err(_) => {
            logging::log(
                config.log_level,
                LogSeverity::Error,
                &config.service_name,
                "greeting failed",
            );
            std::process::exit(1);
        }
    }
    logging::log(
        config.log_level,
        LogSeverity::Information,
        &config.service_name,
        "service finished",
    );
}
