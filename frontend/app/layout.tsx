import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Incident Response Agent",
  description:
    "A stateful AI workflow for evidence-backed incident analysis.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}