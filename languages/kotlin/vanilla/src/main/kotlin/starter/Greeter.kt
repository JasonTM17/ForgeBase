package starter

/**
 * Example domain service. It exists to demonstrate the shape a real service
 * takes (validation -> behavior), not to carry business meaning — replace
 * it when copying the template out.
 */
class Greeter {
    fun greet(name: String): String {
        require(name.isNotBlank()) { "name must not be empty" }
        return "Hello, $name!"
    }
}
