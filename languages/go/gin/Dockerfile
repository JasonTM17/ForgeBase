# syntax=docker/dockerfile:1
FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o api ./cmd/api

FROM gcr.io/distroless/static-debian12 AS runtime
COPY --from=builder /app/api /api
EXPOSE 8000
ENTRYPOINT ["/api"]
