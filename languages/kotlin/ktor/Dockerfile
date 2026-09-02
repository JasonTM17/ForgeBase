# Build stage: compile and assemble the distribution.
FROM gradle:8.14-jdk21 AS build
WORKDIR /src
COPY build.gradle.kts settings.gradle.kts ./
COPY src ./src
RUN gradle installDist --no-daemon

# Runtime stage: minimal JRE image, non-root user, distribution only.
FROM eclipse-temurin:21-jre-alpine AS runtime
RUN adduser --system --uid 10001 app
WORKDIR /app
COPY --from=build /src/build/install/ktor-starter ./
ENV PORT=8080
USER app
EXPOSE 8080
ENTRYPOINT ["bin/ktor-starter"]
