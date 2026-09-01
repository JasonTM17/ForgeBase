#ifndef STARTER_LOGGING_HPP
#define STARTER_LOGGING_HPP

#include "starter/log_severity.hpp"

#include <string>

namespace starter {

// Minimal leveled logger: ISO-8601 UTC timestamp, severity tag, and service
// context on every line. Errors go to stderr.
class Logger {
public:
    Logger(LogSeverity threshold, std::string service);

    void info(const std::string& message) const;
    void warning(const std::string& message) const;
    void error(const std::string& message) const;

private:
    void write(LogSeverity severity, const std::string& message) const;

    LogSeverity threshold_;
    std::string service_;
};

}  // namespace starter

#endif  // STARTER_LOGGING_HPP
