#ifndef STARTER_LOG_SEVERITY_HPP
#define STARTER_LOG_SEVERITY_HPP

#include <optional>
#include <string_view>

namespace starter {

// Severity levels for the built-in console logger, ordered from most to
// least severe. The enumerator order is the severity order.
enum class LogSeverity {
    Critical = 0,
    Error = 1,
    Warning = 2,
    Information = 3,
    Debug = 4,
    Trace = 5,
};

// Parses a case-insensitive level name; nullopt when unknown.
std::optional<LogSeverity> parse_log_severity(std::string_view name);

}  // namespace starter

#endif  // STARTER_LOG_SEVERITY_HPP
