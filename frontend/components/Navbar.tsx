"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <header className="w-full border">
      <ul className="flex justify-between items-center px-[50px] py-2.5 ">
        <li className="logo text-2xl tracking-[-2.5px]">Skill Lantern</li>
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
              Login
            </button>
          </Link>
        </li>
      </ul>
    </header>
  );
}
