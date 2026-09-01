using Starter;
using Xunit;

namespace Starter.Tests;

public class EnvConfigTests
{
    [Fact]
    public void Throws_when_required_variable_is_missing()
    {
        var env = new Dictionary<string, string?>();

        Assert.Throws<EnvConfigException>(() => EnvConfig.FromEnvironment(env));
    }

    [Fact]
    public void Throws_when_required_variable_is_empty()
    {
        var env = new Dictionary<string, string?> { ["SERVICE_NAME"] = "  " };

        Assert.Throws<EnvConfigException>(() => EnvConfig.FromEnvironment(env));
    }

    [Fact]
    public void Defaults_log_level_to_information()
    {
        var config = EnvConfig.FromEnvironment(
            new Dictionary<string, string?> { ["SERVICE_NAME"] = "demo" });

        Assert.Equal(LogSeverity.Information, config.LogLevel);
    }

    [Fact]
    public void Throws_on_unknown_log_level()
    {
        var env = new Dictionary<string, string?>
        {
            ["SERVICE_NAME"] = "demo",
            ["APP_LOG_LEVEL"] = "loud",
        };

        Assert.Throws<EnvConfigException>(() => EnvConfig.FromEnvironment(env));
    }

    [Fact]
    public void Parses_log_level_case_insensitively()
    {
        var env = new Dictionary<string, string?>
        {
            ["SERVICE_NAME"] = "demo",
            ["APP_LOG_LEVEL"] = "warning",
        };

        Assert.Equal(LogSeverity.Warning, EnvConfig.FromEnvironment(env).LogLevel);
    }
}
