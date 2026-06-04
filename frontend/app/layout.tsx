import type { Metadata } from "next";
import "./globals.css";
import SessionProvider from "@/components/SessionProvider";

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
    <html lang="en" className="scroll-smooth" suppressHydrationWarning>
      <body className="antialiased bg-background text-foreground" suppressHydrationWarning>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
