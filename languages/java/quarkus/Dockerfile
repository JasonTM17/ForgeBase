# syntax=docker/dockerfile:1
FROM maven:3.9-eclipse-temurin-21-jammy AS builder
WORKDIR /app
COPY pom.xml ./
RUN mvn -q dependency:go-offline
COPY src ./src
RUN mvn -q package -DskipTests

FROM eclipse-temurin:21-jre-jammy AS runtime
RUN groupadd --system app && useradd --system --gid app app
WORKDIR /app
COPY --from=builder --chown=app:app /app/target/quarkus-app ./quarkus-app
USER app
EXPOSE 8000
ENTRYPOINT ["java", "-jar", "quarkus-app/quarkus-run.jar"]
