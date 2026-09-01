import React from "react";
import { StyleSheet, Text, View } from "react-native";

export interface GreetingCardProps {
  name: string;
  greeting: string;
}

// Example component demonstrating the idiomatic prop -> render shape with
// generic-domain content only. Replace it when copying the template out.
export function GreetingCard({ name, greeting }: GreetingCardProps) {
  return (
    <View style={styles.card} testID="greeting-card">
      <Text style={styles.title}>{greeting}</Text>
      <Text style={styles.subtitle}>Served by {name}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 20,
    gap: 6,
    alignItems: "center",
  },
  title: {
    fontSize: 22,
    fontWeight: "600",
  },
  subtitle: {
    fontSize: 14,
    color: "#555555",
  },
});
