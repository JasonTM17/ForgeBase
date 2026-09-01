/* setenv/unsetenv are POSIX; expose them under strict -std=c++20. */
#if !defined(_WIN32)
#define _POSIX_C_SOURCE 200809L
#endif

#include "starter/config.hpp"
#include "starter/greeter.hpp"
#include "starter/log_severity.hpp"
#include "starter/logging.hpp"

#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>

// Dependency-free test binary registered with CTest. CHECK records the
// failing test and line, then stops the binary with a non-zero exit.
namespace {

int failures = 0;

#define CHECK(condition)                                                       \
    do {                                                                       \
        if (!(condition)) {                                                    \
            std::cerr << "FAIL " << __func__ << ':' << __LINE__ << ": "       \
                      << #condition << '\n';                                   \
            ++failures;                                                        \
            return;                                                            \
        }                                                                      \
    } while (0)

}  // namespace

void test_log_severity_parses_known_names()
{
    CHECK(starter::parse_log_severity("critical") ==
          starter::LogSeverity::Critical);
    CHECK(starter::parse_log_severity("Information") ==
          starter::LogSeverity::Information);
    CHECK(starter::parse_log_severity("TRACE") == starter::LogSeverity::Trace);
}

void test_log_severity_rejects_unknown()
{
    CHECK(!starter::parse_log_severity("loud").has_value());
    CHECK(!starter::parse_log_severity("").has_value());
}

void test_config_requires_service_name()
{
    ::unsetenv("SERVICE_NAME");

    bool threw = false;
    try {
        starter::Config::from_environment();
    } catch (const starter::config_error& error) {
        threw = true;
        CHECK(std::string(error.what()).find("SERVICE_NAME") !=
              std::string::npos);
    }
    CHECK(threw);
}

void test_config_defaults_log_level()
{
    setenv("SERVICE_NAME", "demo", 1);
    unsetenv("APP_LOG_LEVEL");

    const auto config = starter::Config::from_environment();
    CHECK(config.service_name == "demo");
    CHECK(config.log_level == starter::LogSeverity::Information);
}

void test_config_rejects_unknown_level()
{
    setenv("SERVICE_NAME", "demo", 1);
    setenv("APP_LOG_LEVEL", "loud", 1);

    bool threw = false;
    try {
        starter::Config::from_environment();
    } catch (const starter::config_error&) {
        threw = true;
    }
    CHECK(threw);
}

void test_greeter_greets_and_rejects_empty()
{
    const starter::Greeter greeter;
    CHECK(greeter.greet("ForgeBase") == "Hello, ForgeBase!");
    bool threw = false;
    try {
        greeter.greet("   ");
    } catch (const std::invalid_argument&) {
        threw = true;
    }
    CHECK(threw);
}

int main()
{
    test_log_severity_parses_known_names();
    test_log_severity_rejects_unknown();
    test_config_requires_service_name();
    test_config_defaults_log_level();
    test_config_rejects_unknown_level();
    test_greeter_greets_and_rejects_empty();

    if (failures > 0) {
        std::cerr << failures << " check(s) failed\n";
        return 1;
    }
    std::cout << "all starter tests passed\n";
    return 0;
}
