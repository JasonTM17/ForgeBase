# frozen_string_literal: true

# Example domain service. It exists to demonstrate the shape a real service
# takes (validation -> behavior), not to carry business meaning — replace
# it when copying the template out.

module Starter
  class Greeter
    def greet(name)
      raise ArgumentError, 'name must not be empty' if name.strip.empty?

      "Hello, #{name}!"
    end
  end
end
