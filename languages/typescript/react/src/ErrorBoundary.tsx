import { Component, type ReactNode } from "react";

/**
 * Error boundary — the single place component-tree crashes become a usable
 * UI instead of a blank screen. In production the detail is logged
 * server-side; here we render a safe fallback.
 */
interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error): void {
    // Send to your error tracker in production.
    console.error("[ErrorBoundary]", error);
  }

  render(): ReactNode {
    if (this.state.error) {
      return (
        <div role="alert">
          <h1>Something went wrong</h1>
          <pre>{this.state.error.message}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}
