#include "starter/greeter.hpp"

#include <algorithm>
#include <cctype>

namespace starter {

std::string Greeter::greet(const std::string& name) const
{
    const bool has_content =
        std::any_of(name.begin(), name.end(), [](unsigned char character) {
            return !std::isspace(character);
        });
    if (!has_content) {
        throw std::invalid_argument("name must not be empty");
    }

    return "Hello, " + name + "!";
}

}  // namespace starter
