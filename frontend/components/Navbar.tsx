"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <header
      className={`fixed w-full top-0 left-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-white/80 backdrop-blur-lg shadow-sm border-b border-neutral-200/50"
          : "bg-transparent"
      }`}
    >
      <nav className="container-custom">
        <div className="flex justify-between items-center h-16 md:h-20">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-neutral-900 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">SL</span>
            </div>
            <span className="text-xl font-semibold tracking-tight">
              Skill Lantern
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <Link
              href="/features"
              className={`text-sm transition-colors ${pathname === "/features" ? "text-neutral-900 font-medium" : "text-neutral-600 hover:text-neutral-900"}`}
            >
              Features
            </Link>
            <Link
              href="/howitworks"
              className={`text-sm transition-colors ${pathname === "/howitworks" ? "text-neutral-900 font-medium" : "text-neutral-600 hover:text-neutral-900"}`}
            >
              How it Works
            </Link>
            <Link
              href="/contact"
              className={`text-sm transition-colors ${pathname === "/contact" ? "text-neutral-900 font-medium" : "text-neutral-600 hover:text-neutral-900"}`}
            >
              Contact
            </Link>
          </div>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-4">
            <Link
              href="/registration/login"
              className="btn-primary text-sm"
            >
              Sign In
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isMobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-neutral-200">
            <div className="flex flex-col gap-4">
              <Link
                href="/features"
                className={`text-sm transition-colors py-2 ${pathname === "/features" ? "text-neutral-900 font-medium" : "text-neutral-600 hover:text-neutral-900"}`}
              >
                Features
              </Link>
              <Link
                href="/howitworks"
                className={`text-sm transition-colors py-2 ${pathname === "/howitworks" ? "text-neutral-900 font-medium" : "text-neutral-600 hover:text-neutral-900"}`}
              >
                How it Works
              </Link>
              <Link
                href="/contact"
                className={`text-sm transition-colors py-2 ${pathname === "/contact" ? "text-neutral-900 font-medium" : "text-neutral-600 hover:text-neutral-900"}`}
              >
                Contact
              </Link>
              <Link
                href="/registration/login"
                className="btn-primary text-sm text-center mt-2"
              >
                Sign In
              </Link>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}
