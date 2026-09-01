//! Severity levels and a minimal leveled logger: ISO-8601 UTC timestamp,
//! severity tag, and service context on every line. Errors go to stderr.
//! Replace with `tracing` + `tracing-actix-web` when the copied-out project
//! needs richer sinks.

use std::io::Write;
use std::time::{SystemTime, UNIX_EPOCH};

/// Severity levels, ordered from most to least severe.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum LogSeverity {
    Critical,
    Error,
    Warning,
    Information,
    Debug,
    Trace,
}

impl LogSeverity {
    /// Case-insensitive name parsing; `None` when unknown.
    pub fn parse(name: &str) -> Option<Self> {
        let lowered = name.to_ascii_lowercase();
        match lowered.as_str() {
            "critical" => Some(Self::Critical),
            "error" => Some(Self::Error),
            "warning" => Some(Self::Warning),
            "information" => Some(Self::Information),
            "debug" => Some(Self::Debug),
            "trace" => Some(Self::Trace),
            _ => None,
        }
    }

    /// Short uppercase tag used in log lines, e.g. "INF".
    pub fn tag(self) -> &'static str {
        match self {
            Self::Critical => "CRI",
            Self::Error => "ERR",
            Self::Warning => "WAR",
            Self::Information => "INF",
            Self::Debug => "DEB",
            Self::Trace => "TRA",
        }
    }
}

/// Writes `msg` at `severity` when the threshold allows it.
pub fn log(threshold: LogSeverity, severity: LogSeverity, service: &str, msg: &str) {
    if severity > threshold {
        return;
    }

    let line = format!(
        "{} [{}] service={} {}\n",
        iso_utc_now(),
        severity.tag(),
        service,
        msg
    );
    if severity <= LogSeverity::Error {
        let _ = std::io::stderr().write_all(line.as_bytes());
    } else {
        let _ = std::io::stdout().write_all(line.as_bytes());
    }
}

/// ISO-8601 UTC timestamp without external crates (civil-from-days).
pub fn iso_utc_now() -> String {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default();
    let secs = now.as_secs() as i64;
    let (year, month, day) = civil_from_days(secs.div_euclid(86_400));
    let rem = secs.rem_euclid(86_400);
    format!(
        "{year:04}-{month:02}-{day:02}T{:02}:{:02}:{:02}Z",
        rem / 3600,
        (rem % 3600) / 60,
        rem % 60
    )
}

fn civil_from_days(days: i64) -> (i64, u32, u32) {
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097) as u64;
    let yoe = (doe - doe / 1_460 + doe / 36_524 - doe / 146_096) / 365;
    let year = yoe as i64 + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let day = (doy - (153 * mp + 2) / 5 + 1) as u32;
    let month = if mp < 10 { mp + 3 } else { mp - 9 } as u32;
    (if month <= 2 { year + 1 } else { year }, month, day)
}
