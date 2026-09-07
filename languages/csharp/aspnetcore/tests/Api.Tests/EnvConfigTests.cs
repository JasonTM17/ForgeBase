using Api;
using Xunit;

namespace Api.Tests;

/// <summary>Unit tests for the fail-fast configuration parser: every invalid
/// APP_LOG_LEVEL shape — unknown names, numbers, flag combinations — and every
/// invalid PORT must abort startup with EnvConfigException.</summary>
public class EnvConfigTests
{
    public static TheoryData<string> InvalidLogLevels => new()
    {
        "loud", "999", "None", "Error,Warning",
    };

    [Theory]
    [MemberData(nameof(InvalidLogLevels))]
    public void Invalid_log_levels_fail_fast(string value)
    {
        var environment = new Dictionary<string, string?>
        {
            ["SERVICE_NAME"] = "api",
            ["APP_LOG_LEVEL"] = value,
        };

        Assert.Throws<EnvConfigException>(
            () => EnvConfig.FromEnvironment(environment));
    }

    [Theory]
    [InlineData("Information", Microsoft.Extensions.Logging.LogLevel.Information)]
    [InlineData("debug", Microsoft.Extensions.Logging.LogLevel.Debug)]
    public void Valid_log_levels_parse_case_insensitively(
        string value,
        Microsoft.Extensions.Logging.LogLevel expected)
    {
        var environment = new Dictionary<string, string?>
        {
            ["SERVICE_NAME"] = "api",
            ["APP_LOG_LEVEL"] = value,
        };

        var config = EnvConfig.FromEnvironment(environment);

        Assert.Equal(expected, config.LogLevel);
    }

    [Theory]
    [InlineData("0")]
    [InlineData("65536")]
    [InlineData("http")]
    public void Invalid_ports_fail_fast(string value)
    {
        var environment = new Dictionary<string, string?>
        {
            ["SERVICE_NAME"] = "api",
            ["PORT"] = value,
        };

        Assert.Throws<EnvConfigException>(
            () => EnvConfig.FromEnvironment(environment));
    }
}
