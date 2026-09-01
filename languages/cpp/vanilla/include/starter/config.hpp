#ifndef STARTER_CONFIG_HPP
#define STARTER_CONFIG_HPP

#include "starter/log_severity.hpp"

#include <stdexcept>
#include <string>

namespace starter {

// Fail-fast configuration: missing required variables or values that fail
// validation abort startup before any real work happens.
struct Config {
    std::string service_name;
    LogSeverity log_level{LogSeverity::Information};

    // Reads the process environment; throws config_error with a
    // human-readable message when the configuration is invalid.
    static Config from_environment();
};

// Raised only for configuration problems, so hosts can catch it and exit
// with a clean message instead of a stack trace.
class config_error : public std::runtime_error {
public:
    explicit config_error(const std::string& message)
        : std::runtime_error(message) {}
};

}  // namespace starter

#endif  // STARTER_CONFIG_HPP
