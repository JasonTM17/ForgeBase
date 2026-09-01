import { render } from "@testing-library/react-native";
import React from "react";

import { GreetingCard } from "../components/GreetingCard";

describe("GreetingCard", () => {
  it("renders the greeting and the serving name", async () => {
    const screen = await render(
      <GreetingCard name="ForgeBase" greeting="Hello, ForgeBase!" />,
    );

    expect(screen.getByText("Hello, ForgeBase!")).toBeTruthy();
    expect(screen.getByText("Served by ForgeBase")).toBeTruthy();
  });

  it("exposes the card through its testID", async () => {
    const screen = await render(<GreetingCard name="x" greeting="hi" />);

    expect(screen.getByTestId("greeting-card")).toBeTruthy();
  });
});
