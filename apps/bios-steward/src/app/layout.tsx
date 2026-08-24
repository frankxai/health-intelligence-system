import type { Metadata } from "next";
import { Figtree, Fraunces, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  display: "swap",
});

const figtree = Figtree({
  subsets: ["latin"],
  variable: "--font-figtree",
  display: "swap",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
  display: "swap",
});

export const metadata: Metadata = {
  title: "BIOS Steward — synthetic safety preview",
  description:
    "Read-only synthetic evidence-contract preview. No health input, storage, protocol execution, or export.",
  applicationName: "BIOS Steward synthetic preview",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${fraunces.variable} ${figtree.variable} ${jetbrains.variable}`}>{children}</body>
    </html>
  );
}
