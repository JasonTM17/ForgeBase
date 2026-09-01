// Tests import the config module; give it a valid environment before the
// app code loads, mirroring the fail-fast contract under normal startup.
process.env.EXPO_PUBLIC_SERVICE_NAME ??= "test-service";
