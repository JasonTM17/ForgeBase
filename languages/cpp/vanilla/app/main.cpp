#include "starter/config.hpp"
#include "starter/greeter.hpp"
#include "starter/logging.hpp"

#include <iostream>

// Fail-fast demo: a missing or invalid configuration variable exits with a
// clean message and a non-zero code instead of a stack trace.
int main()
{
    starter::Config config;
    try {
        config = starter::Config::from_environment();
    } catch (const starter::config_error& error) {
        std::cerr << "configuration error: " << error.what() << '\n';
        return 2;
    }

    const starter::Logger logger(config.log_level, config.service_name);
    logger.info("service starting");
    std::cout << starter::Greeter().greet("ForgeBase") << '\n';
    logger.info("service finished");
    return 0;
}
