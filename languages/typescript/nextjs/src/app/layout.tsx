export const metadata = {
  title: "ForgeBase Next.js Starter",
  description: "Production-oriented Next.js base",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
