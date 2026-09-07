using Microsoft.Extensions.Logging;

namespace Api;

/// <summary>Fail-fast configuration: the API refuses to start on missing or
/// invalid settings so misconfiguration is never discovered through request
/// traffic. Values are read from the process environment (the deployment
/// contract), not from appsettings.json.</summary>
public sealed record EnvConfig(string ServiceName, LogLevel LogLevel, int Port)
{
    public static EnvConfig FromEnvironment() =>
        FromEnvironment(Environment.GetEnvironmentVariables()
            .OfType<System.Collections.DictionaryEntry>()
            .ToDictionary(
                e => (string)e.Key,
                e => e.Value as string,
                StringComparer.Ordinal));

    public static EnvConfig FromEnvironment(
        IReadOnlyDictionary<string, string?> environment)
    {
        var serviceName = Required(environment, "SERVICE_NAME");
        var logLevel = ParseLogLevel(
            Optional(environment, "APP_LOG_LEVEL", "Information"));
        var port = ParsePort(Optional(environment, "PORT", "8080"));
        return new EnvConfig(serviceName, logLevel, port);
    }

    private static LogLevel ParseLogLevel(string value)
    {
        var trimmed = value.Trim();
        // Enum.TryParse also accepts numbers and flag combinations ("Error,
        // Warning"); require a single defined level name instead.
        if (trimmed.Contains(',') ||
            !Enum.TryParse<LogLevel>(trimmed, ignoreCase: true, out var level) ||
            level == LogLevel.None ||
            !Enum.IsDefined(level))
        {
            var valid = string.Join(", ",
                Enum.GetNames<LogLevel>().Where(n => n != nameof(LogLevel.None)));
            throw new EnvConfigException(
                $"APP_LOG_LEVEL '{value}' is invalid. Valid values: {valid}.");
        }

        return level;
    }

    private static int ParsePort(string value)
    {
        if (!int.TryParse(value, out var port) || port is < 1 or > 65535)
        {
            throw new EnvConfigException(
                $"PORT '{value}' is invalid. Expected an integer in 1..65535.");
        }

        return port;
    }

    private static string Required(IReadOnlyDictionary<string, string?> env, string name)
    {
        if (!env.TryGetValue(name, out var value) ||
            string.IsNullOrWhiteSpace(value))
        {
            throw new EnvConfigException(
                $"required environment variable {name} is missing or empty");
        }

        return value;
    }

    private static string Optional(
        IReadOnlyDictionary<string, string?> env, string name, string fallback) =>
        env.TryGetValue(name, out var value) && !string.IsNullOrWhiteSpace(value)
            ? value
            : fallback;
}

/// <summary>Raised only for configuration problems; Program catches it and
/// exits with a clean message instead of a stack trace.</summary>
public sealed class EnvConfigException : Exception
{
    public EnvConfigException(string message) : base(message) { }
}
