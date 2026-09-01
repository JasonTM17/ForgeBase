using Api;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;

// Fail fast before the host is built: a broken deployment configuration must
// never turn into runtime request failures.
EnvConfig config;
try
{
    config = EnvConfig.FromEnvironment();
}
catch (EnvConfigException ex)
{
    Console.Error.WriteLine($"configuration error: {ex.Message}");
    return 2;
}

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls($"http://0.0.0.0:{config.Port}");

builder.Logging.ClearProviders();
builder.Logging.AddSimpleConsole(options =>
{
    options.SingleLine = true;
    options.TimestampFormat = "yyyy-MM-ddTHH:mm:ss.fffZ ";
    options.UseUtcTimestamp = true;
});
builder.Logging.SetMinimumLevel(config.LogLevel);

// RFC 9457 ProblemDetails for unhandled exceptions and unmatched routes.
builder.Services.AddProblemDetails();
builder.Services.AddHealthChecks();

var app = builder.Build();

// Unhandled exceptions -> ProblemDetails without internal details; unmatched
// routes -> ProblemDetails via the status-code page.
app.UseExceptionHandler();
app.UseStatusCodePages();

var logger = app.Logger;
logger.LogInformation("service {ServiceName} listening on port {Port}",
    config.ServiceName, config.Port);
app.Lifetime.ApplicationStopping.Register(
    () => logger.LogInformation("service {ServiceName} shutting down",
        config.ServiceName));

// Ecosystem-idiomatic probes: the health-checks middleware response is the
// ASP.NET Core convention, tagged variants cover liveness and readiness.
app.MapHealthChecks("/health");
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("live"),
});
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready"),
});

// Example resource: request -> validation -> store -> response, with
// RFC 9457 ProblemDetails on the error paths.
app.MapWidgetEndpoints();

app.Run();
return 0;

// Exposes Program to WebApplicationFactory-based integration tests.
public partial class Program { }
