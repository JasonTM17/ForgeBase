plugins {
    kotlin("jvm") version "2.2.20"
    application
}

group = "com.example.starter"
version = "0.1.0"

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(21)
}

dependencies {
    testImplementation(kotlin("test"))
}

application {
    mainClass.set("starter.MainKt")
}

tasks.test {
    useJUnitPlatform()
}
