import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";

import { ErrorBoundary } from "./src/components/ErrorBoundary";
import { GreetingCard } from "./src/components/GreetingCard";
import { config } from "./src/config";

export default function App() {
  return (
    <ErrorBoundary>
      <View style={styles.container}>
        <StatusBar style="auto" />
        <Text style={styles.heading}>{config.serviceName}</Text>
        <GreetingCard name="ForgeBase" greeting="Hello, ForgeBase!" />
      </View>
    </ErrorBoundary>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f4f4f5",
    alignItems: "center",
    justifyContent: "center",
    gap: 24,
  },
  heading: {
    fontSize: 18,
    fontWeight: "600",
    color: "#333333",
  },
});
