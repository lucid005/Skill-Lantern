import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import "./globals.css";
import SessionProvider from "@/components/SessionProvider";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-montserrat",
});

export const metadata: Metadata = {
  title: "Skill Lantern | AI-Powered Career Recommendations",
  description: "Discover your perfect career path with Skill Lantern. Our AI analyzes your skills, interests, and goals to provide personalized career recommendations and learning roadmaps.",
  keywords: ["career recommendation", "AI career guidance", "skill assessment", "career path", "learning roadmap", "career planning"],
  authors: [{ name: "Skill Lantern" }],
  openGraph: {
    title: "Skill Lantern | AI-Powered Career Recommendations",
    description: "Discover your perfect career path with personalized AI-powered recommendations.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body
        className={`${inter.variable} ${montserrat.variable} antialiased bg-background text-foreground`}
      >
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}