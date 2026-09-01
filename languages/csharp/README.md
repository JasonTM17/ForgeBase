# C# Starters

Self-contained C# basecode templates. Copy a starter folder out of this
repository and it runs as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Zero-dependency library/CLI base: fail-fast env config, structured console logging, example service, xunit tests |

## Verification strategy

- `vanilla` is verified locally with the .NET SDK (build, test, format check).
- `aspnetcore` (roadmap of this phase) adds Docker-based verification on top.

## Copying a starter out

```bash
cp -r languages/csharp/vanilla /path/to/my-project
cd /path/to/my-project
# rename the solution/projects/namespaces from "Starter" to your product name
dotnet build
dotnet test
```
