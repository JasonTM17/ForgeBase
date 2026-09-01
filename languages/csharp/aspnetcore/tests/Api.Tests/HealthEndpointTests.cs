using System.Net;
using System.Net.Http.Json;
using Api;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace Api.Tests;

/// <summary>Integration tests over the real host pipeline via
/// WebApplicationFactory: proves bootstrap, probe routing, and the widget
/// request/response/error contract end to end.</summary>
public class HealthEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    static HealthEndpointTests()
    {
        // The API fails fast on missing configuration by design; give the
        // test host a valid configuration before Program runs.
        Environment.SetEnvironmentVariable("SERVICE_NAME", "api-tests");
        Environment.SetEnvironmentVariable("PORT", "8080");
    }

    private readonly WebApplicationFactory<Program> _factory;

    public HealthEndpointTests(WebApplicationFactory<Program> factory) =>
        _factory = factory;

    [Theory]
    [InlineData("/health")]
    [InlineData("/health/live")]
    [InlineData("/health/ready")]
    public async Task Health_probes_return_healthy(string path)
    {
        var client = _factory.CreateClient();

        var response = await client.GetAsync(path);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        Assert.Contains("Healthy", await response.Content.ReadAsStringAsync());
    }

    [Fact]
    public async Task Unknown_route_returns_problem_details()
    {
        var client = _factory.CreateClient();

        var response = await client.GetAsync("/nope");
        var problem = await response.Content.ReadFromJsonAsync<ValidationProblemDetailsShape>();

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        Assert.Equal("application/problem+json", response.Content.Headers.ContentType!.MediaType);
        Assert.Equal(404, problem!.Status);
    }

    [Fact]
    public async Task Widget_flow_validates_creates_and_rejects_bad_input()
    {
        var client = _factory.CreateClient();

        var created = await client.PostAsJsonAsync("/api/widgets", new { name = "anvil" });
        Assert.Equal(HttpStatusCode.Created, created.StatusCode);
        var widget = await created.Content.ReadFromJsonAsync<WidgetShape>();
        Assert.False(widget!.Id == Guid.Empty);

        var fetched = await client.GetAsync($"/api/widgets/{widget.Id}");
        Assert.Equal(HttpStatusCode.OK, fetched.StatusCode);

        var missing = await client.GetAsync($"/api/widgets/{Guid.NewGuid()}");
        Assert.Equal(HttpStatusCode.NotFound, missing.StatusCode);
        Assert.Equal("application/problem+json", missing.Content.Headers.ContentType!.MediaType);

        var invalid = await client.PostAsJsonAsync("/api/widgets", new { name = "" });
        Assert.Equal(HttpStatusCode.BadRequest, invalid.StatusCode);
        Assert.Equal("application/problem+json", invalid.Content.Headers.ContentType!.MediaType);
    }

    [Fact]
    public void Configuration_fails_fast_on_missing_service_name()
    {
        Assert.Throws<EnvConfigException>(
            () => EnvConfig.FromEnvironment(new Dictionary<string, string?>()));
    }

    private sealed record WidgetShape(Guid Id, string Name);

    private sealed class ValidationProblemDetailsShape
    {
        public int Status { get; init; }
        public string Title { get; init; } = string.Empty;
    }
}
