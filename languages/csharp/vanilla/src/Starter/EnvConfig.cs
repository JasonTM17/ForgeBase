namespace Starter;

/// <summary>Fail-fast configuration: missing required variables or values
/// that fail validation abort startup before any real work happens, so
/// misconfiguration is never discovered in production traffic.</summary>
public sealed record EnvConfig(string ServiceName, LogSeverity LogLevel)
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
        var logLevel = Optional(environment, "APP_LOG_LEVEL", "Information");
        if (!Enum.TryParse<LogSeverity>(logLevel, ignoreCase: true, out var severity))
        {
            var valid = string.Join(", ", Enum.GetNames<LogSeverity>());
            throw new EnvConfigException(
                $"APP_LOG_LEVEL '{logLevel}' is invalid. Valid values: {valid}.");
        }

        return new EnvConfig(serviceName, severity);
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

/// <summary>Raised only for configuration problems, so hosts can catch it and
/// exit with a clean message instead of a stack trace.</summary>
public sealed class EnvConfigException : Exception
{
    public EnvConfigException(string message) : base(message) { }
}
