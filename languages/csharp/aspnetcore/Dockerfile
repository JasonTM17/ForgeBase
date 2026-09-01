# Build stage: restore and publish a self-contained release output.
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /src
COPY src/Api/Api.csproj ./
RUN dotnet restore
COPY src/Api/ ./
RUN dotnet publish -c Release -o /app --no-restore

# Runtime stage: minimal ASP.NET Core image, non-root user, no source code.
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app
COPY --from=build /app .
ENV PORT=8080
USER $APP_UID
ENTRYPOINT ["dotnet", "Api.dll"]
