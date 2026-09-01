#include "starter/log_severity.hpp"

#include <cctype>
#include <iterator>

namespace starter {
namespace {

constexpr std::string_view kNames[] = {
    "critical", "error", "warning", "information", "debug", "trace"
};

}  // namespace

std::optional<LogSeverity> parse_log_severity(std::string_view name)
{
    std::string lowered;
    lowered.reserve(name.size());
    for (char character : name) {
        lowered.push_back(
            static_cast<char>(std::tolower(static_cast<unsigned char>(character))));
    }

    for (std::size_t i = 0; i < std::size(kNames); ++i) {
        if (lowered == kNames[i]) {
            return static_cast<LogSeverity>(i);
        }
    }
    return std::nullopt;
}

}  // namespace starter
