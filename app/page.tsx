"use client"

import Navbar from "@/components/Navbar";
import Home from "./home/page";
import Footer from "@/components/Footer";

export default function page() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="grow">
        <Home />
      </main>
      <Footer />
    </div>
  );
}
