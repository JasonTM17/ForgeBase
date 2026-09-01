//! Graceful shutdown: SIGTERM/SIGINT finish in-flight requests instead of
//! dropping them.

use tokio::signal::unix::{signal, SignalKind};

pub async fn shutdown_signal() {
    let mut sigterm = signal(SignalKind::terminate()).expect("install SIGTERM handler");
    let mut sigint = signal(SignalKind::interrupt()).expect("install SIGINT handler");

    tokio::select! {
        _ = sigterm.recv() => {},
        _ = sigint.recv() => {},
    }
}
