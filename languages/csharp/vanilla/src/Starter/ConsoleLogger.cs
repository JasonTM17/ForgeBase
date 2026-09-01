namespace Starter;

/// <summary>Minimal leveled logger: ISO-8601 timestamp, severity tag, and
/// service context on every line. Errors go to stderr so redirection keeps
/// diagnostics out of data pipelines. Replace with a structured logging
/// library when the copied-out project needs richer sinks.</summary>
public sealed class ConsoleLogger
{
    private readonly LogSeverity _threshold;
    private readonly string _service;

    public ConsoleLogger(LogSeverity threshold, string service)
    {
        _threshold = threshold;
        _service = service;
    }

    public void Info(string message) => Write(LogSeverity.Information, message);

    public void Warning(string message) => Write(LogSeverity.Warning, message);

    public void Error(string message) => Write(LogSeverity.Error, message);

    private void Write(LogSeverity severity, string message)
    {
        if (severity > _threshold)
        {
            return;
        }

        var line = $"{DateTimeOffset.UtcNow:O} " +
                   $"[{severity.ToString().ToUpperInvariant()![..3]}] " +
                   $"service={_service} {message}";
        if (severity <= LogSeverity.Error)
        {
            Console.Error.WriteLine(line);
        }
        else
        {
            Console.Out.WriteLine(line);
        }
    }
}
