import React from "react";
import { StyleSheet, Text, View } from "react-native";

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

// App-level error boundary: an unhandled render error shows a recoverable
// fallback instead of crashing to the native red screen in production.
export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error): void {
    // Replace with the project's crash reporting hook when copying out.
    console.error("Unhandled render error:", error);
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      return (
        <View style={styles.container} testID="error-fallback">
          <Text style={styles.title}>Something went wrong</Text>
          <Text style={styles.message}>Please restart the app.</Text>
        </View>
      );
    }
    return this.props.children;
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
  },
  title: {
    fontSize: 20,
    fontWeight: "600",
  },
  message: {
    marginTop: 8,
    color: "#555555",
  },
});
