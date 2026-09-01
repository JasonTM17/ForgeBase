namespace Starter;

/// <summary>Severity levels for the built-in console logger, ordered from
/// most to least severe. Keeping the enum local keeps the starter
/// dependency-free; swap for a logging library when the copied-out project
/// grows.</summary>
public enum LogSeverity
{
    Critical = 0,
    Error = 1,
    Warning = 2,
    Information = 3,
    Debug = 4,
    Trace = 5,
}
