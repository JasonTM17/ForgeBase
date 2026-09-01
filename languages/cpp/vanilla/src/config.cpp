#include "starter/config.hpp"

#include <cstdlib>

namespace starter {
namespace {

std::string required(const char* name)
{
    const char* value = std::getenv(name);
    if (value == nullptr || *value == '\0') {
        throw config_error(std::string("required environment variable ") +
                           name + " is missing or empty");
    }
    return value;
}

std::string optional(const char* name, std::string fallback)
{
    const char* value = std::getenv(name);
    return (value != nullptr && *value != '\0') ? value : fallback;
}

}  // namespace

Config Config::from_environment()
{
    Config config;
    config.service_name = required("SERVICE_NAME");

    const auto level = parse_log_severity(
        optional("APP_LOG_LEVEL", "information"));
    if (!level.has_value()) {
        throw config_error(
            "APP_LOG_LEVEL is invalid. Valid values: critical, error, "
            "warning, information, debug, trace.");
    }
    config.log_level = *level;
    return config;
}

}  // namespace starter
