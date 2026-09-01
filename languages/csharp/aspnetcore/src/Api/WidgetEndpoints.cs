using System.Collections.Concurrent;
using System.Text.Json.Serialization;

namespace Api;

public sealed record Widget(
    [property: JsonPropertyName("id")] Guid Id,
    [property: JsonPropertyName("name")] string Name);

/// <summary>Example resource demonstrating the request -> validation ->
/// store -> response flow with RFC 9457 error responses. The in-memory store
/// is deliberate: Phase-1 templates carry no database layer.</summary>
public static class WidgetEndpoints
{
    private static readonly ConcurrentDictionary<Guid, Widget> Widgets = new();

    public static void MapWidgetEndpoints(this IEndpointRouteBuilder app)
    {
        var widgets = app.MapGroup("/api/widgets").WithTags("Widgets");

        widgets.MapPost("/", async (HttpRequest request) =>
        {
            var body = await request.ReadFromJsonAsync<CreateWidgetRequest>();
            if (body is null || string.IsNullOrWhiteSpace(body.Name))
            {
                return Results.ValidationProblem(new Dictionary<string, string[]>
                {
                    ["name"] = ["name is required"],
                });
            }

            var widget = new Widget(Guid.NewGuid(), body.Name);
            Widgets[widget.Id] = widget;
            return Results.Created($"/api/widgets/{widget.Id}", widget);
        });

        widgets.MapGet("/", () => Results.Ok(Widgets.Values.OrderBy(w => w.Name)));

        widgets.MapGet("/{id:guid}", (Guid id) =>
            Widgets.TryGetValue(id, out var widget)
                ? Results.Ok(widget)
                : Results.Problem(
                    statusCode: StatusCodes.Status404NotFound,
                    title: "widget not found"));

        widgets.MapDelete("/{id:guid}", (Guid id) =>
            Widgets.TryRemove(id, out _)
                ? Results.NoContent()
                : Results.Problem(
                    statusCode: StatusCodes.Status404NotFound,
                    title: "widget not found"));
    }

    private sealed record CreateWidgetRequest(string? Name);
}
