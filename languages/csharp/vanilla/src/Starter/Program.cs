using Starter;

// Fail-fast demo: a missing or invalid configuration variable exits with a
// clean message and a non-zero code instead of a stack trace.
try
{
    var config = EnvConfig.FromEnvironment();
    var logger = new ConsoleLogger(config.LogLevel, config.ServiceName);

    logger.Info("service starting");
    var greeter = new Greeter();
    Console.WriteLine(greeter.Greet("ForgeBase"));
    logger.Info("service finished");
    return 0;
}
catch (EnvConfigException ex)
{
    Console.Error.WriteLine($"configuration error: {ex.Message}");
    return 2;
}
