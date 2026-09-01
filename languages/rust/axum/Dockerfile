# Build stage: compile the release binary.
FROM rust:1-bookworm AS build
WORKDIR /src
COPY Cargo.toml Cargo.lock ./
COPY src ./src
COPY tests ./tests
RUN cargo build --release

# Runtime stage: minimal Debian image, non-root user, binary only.
FROM debian:bookworm-slim AS runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 10001 --no-create-home app
WORKDIR /app
COPY --from=build /src/target/release/axum-starter /app/server
ENV PORT=8080
USER app
EXPOSE 8080
ENTRYPOINT ["/app/server"]
