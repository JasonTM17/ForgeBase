using Starter;
using Xunit;

namespace Starter.Tests;

public class GreeterTests
{
    [Fact]
    public void Greets_by_name()
    {
        Assert.Equal("Hello, ForgeBase!", new Greeter().Greet("ForgeBase"));
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    public void Rejects_empty_names(string name)
    {
        Assert.Throws<ArgumentException>(() => new Greeter().Greet(name));
    }
}
