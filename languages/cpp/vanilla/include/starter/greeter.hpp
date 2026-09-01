#ifndef STARTER_GREETER_HPP
#define STARTER_GREETER_HPP

#include <stdexcept>
#include <string>

namespace starter {

// Example domain service. It exists to demonstrate the shape a real service
// takes (validation -> behavior), not to carry business meaning — replace
// it when copying the template out.
class Greeter {
public:
    // Throws std::invalid_argument for empty or whitespace-only names.
    std::string greet(const std::string& name) const;
};

}  // namespace starter

#endif  // STARTER_GREETER_HPP
