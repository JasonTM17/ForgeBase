/* Use the platform's reentrant UTC conversion under strict C++20. */
#if !defined(_WIN32)
#define _POSIX_C_SOURCE 200809L
#endif

#include "starter/logging.hpp"

#include <chrono>
#include <ctime>
#include <iostream>
#include <iomanip>
#include <sstream>

namespace starter {
namespace {

std::string utc_timestamp()
{
    const auto now = std::chrono::system_clock::now();
    const std::time_t time = std::chrono::system_clock::to_time_t(now);
    std::tm utc{};
#ifdef _WIN32
    if (gmtime_s(&utc, &time) != 0) {
        return "1970-01-01T00:00:00Z";
    }
#else
    gmtime_r(&time, &utc);
#endif
    std::ostringstream stream;
    stream << std::put_time(&utc, "%Y-%m-%dT%H:%M:%SZ");
    return stream.str();
}

constexpr std::string_view kTags[] = {"CRI", "ERR", "WAR", "INF", "DEB", "TRA"};

}  // namespace

Logger::Logger(LogSeverity threshold, std::string service)
    : threshold_(threshold), service_(std::move(service)) {}

void Logger::info(const std::string& message) const
{
    write(LogSeverity::Information, message);
}

void Logger::warning(const std::string& message) const
{
    write(LogSeverity::Warning, message);
}

void Logger::error(const std::string& message) const
{
    write(LogSeverity::Error, message);
}

void Logger::write(LogSeverity severity, const std::string& message) const
{
    if (static_cast<int>(severity) > static_cast<int>(threshold_)) {
        return;
    }

    std::ostream& sink =
        severity <= LogSeverity::Error ? std::cerr : std::cout;
    sink << utc_timestamp() << ' ' << kTags[static_cast<std::size_t>(severity)]
         << " service=" << service_ << ' ' << message << '\n';
}

}  // namespace starter
