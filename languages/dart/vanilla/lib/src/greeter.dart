/// Example domain service. It exists to demonstrate the shape a real service
/// takes (validation -> behavior), not to carry business meaning — replace
/// it when copying the template out.
class Greeter {
  String greet(String name) {
    if (name.trim().isEmpty) {
      throw ArgumentError('name must not be empty');
    }
    return 'Hello, $name!';
  }
}
