"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <header className={`w-full top-0 left-0 bg-[#F7F7F0] z-50 ${isScrolled ? "fixed shadow-md" : "absolute"}`}>
      <ul className="flex justify-between items-center px-[50px] py-2.5 ">
        <li className="logo text-2xl tracking-[-2.5px]"><Link href="/">Skill Lantern</Link></li>
        <li className="text-sm hover:underline">
          <Link href="/features">Features</Link>
        </li>
        <li className="text-sm hover:underline">
          <Link href="/howitworks">How it Works</Link>
        </li>
        <li className="text-sm hover:underline">
          <Link href="/contact ">Contact</Link>
        </li>
        <li>
          <Link href="/registration/login">
            <button className="px-5 py-2 text-sm bg-black text-white rounded-sm cursor-pointer ">
              Log in
            </button>
          </Link>
        </li>
      </ul>
    </header>
  );
}
