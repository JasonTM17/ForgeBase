namespace Starter;

/// <summary>Example domain service. It exists to demonstrate the shape a
/// real service takes (validation -> behavior), not to carry business
/// meaning — replace it when copying the template out.</summary>
public sealed class Greeter
{
    public string Greet(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            throw new ArgumentException(
                "name must not be empty", nameof(name));
        }

        return $"Hello, {name}!";
    }
}
